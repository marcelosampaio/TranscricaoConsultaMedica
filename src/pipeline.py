
import csv
from datetime import datetime
from pathlib import Path
from time import perf_counter

from src.transcrever import carregar_modelo, transcrever_audio
from src.avaliar_transcricao import avaliar_transcricao


DATASET_DIR = (
    Path.home()
    / "PythonFolder"
    / "TranscricaoConsultaMedicaDataSets"
)

AUDIO_DIR = DATASET_DIR / "audios_fornecidos"
REFERENCE_DIR = DATASET_DIR / "transcricoes_fornecidas"

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
TRANSCRIPTIONS_DIR = RESULTS_DIR / "transcricoes"
CSV_FILE = RESULTS_DIR / "avaliacao.csv"


def ler_transcricao_referencia(reference_file):
    content = reference_file.read_bytes()

    if content.startswith((b"\xff\xfe", b"\xfe\xff")):
        return content.decode("utf-16")

    return content.decode("utf-8-sig")


def processar_consultas(consulta_id=None):
    start_datetime = datetime.now()
    start_time = perf_counter()

    print(
        f"Início do processamento: "
        f"{start_datetime:%d/%m/%Y %H:%M:%S}"
    )

    TRANSCRIPTIONS_DIR.mkdir(parents=True, exist_ok=True)

    audio_files = sorted(AUDIO_DIR.glob("*.mp3"))

    if consulta_id:
        audio_files = [
            audio_file
            for audio_file in audio_files
            if audio_file.stem == consulta_id
        ]

        if not audio_files:
            raise FileNotFoundError(
                f"Áudio não encontrado para a consulta {consulta_id}"
            )

    print(f"Consultas encontradas: {len(audio_files)}")

    model = carregar_modelo()

    evaluations = []
    errors = []

    for index, audio_file in enumerate(audio_files, start=1):
        consultation_id = audio_file.stem
        reference_file = REFERENCE_DIR / f"{consultation_id}.txt"

        print(
            f"\n[{index}/{len(audio_files)}] "
            f"Processando {consultation_id}"
        )

        try:
            if not reference_file.is_file():
                raise FileNotFoundError(
                    f"Transcrição de referência não encontrada: {reference_file}"
                )

            transcription = transcrever_audio(audio_file, model)

            reference = ler_transcricao_referencia(reference_file)

            metrics = avaliar_transcricao(reference, transcription)
            metrics["consulta"] = consultation_id

            output_file = TRANSCRIPTIONS_DIR / f"{consultation_id}.txt"
            output_file.write_text(
                transcription + "\n",
                encoding="utf-8",
            )

            evaluations.append(metrics)

            print(f"WER: {metrics['wer']:.2%}")

        except Exception as error:
            errors.append({
                "consulta": consultation_id,
                "erro": str(error),
            })

            print(f"Erro ao processar {consultation_id}: {error}")

    salvar_avaliacoes(evaluations)

    exibir_resumo(evaluations, errors)

    end_datetime = datetime.now()
    elapsed_time = perf_counter() - start_time

    hours, remainder = divmod(int(elapsed_time), 3600)
    minutes, seconds = divmod(remainder, 60)

    print("\n========== TEMPO DE PROCESSAMENTO ==========")
    print(f"Início: {start_datetime:%d/%m/%Y %H:%M:%S}")
    print(f"Fim: {end_datetime:%d/%m/%Y %H:%M:%S}")
    print(f"Tempo total: {hours:02d}:{minutes:02d}:{seconds:02d}")


def salvar_avaliacoes(evaluations):
    fieldnames = [
        "consulta",
        "palavras_referencia",
        "palavras_whisper",
        "hits",
        "substitutions",
        "deletions",
        "insertions",
        "wer",
    ]

    with CSV_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(evaluations)


def exibir_resumo(evaluations, errors):
    total_references = sum(
        item["palavras_referencia"]
        for item in evaluations
    )

    total_errors = sum(
        item["substitutions"]
        + item["deletions"]
        + item["insertions"]
        for item in evaluations
    )

    global_wer = (
        total_errors / total_references
        if total_references
        else 0
    )

    print("\n========== RESULTADO FINAL ==========")
    print(f"Consultas avaliadas: {len(evaluations)}")
    print(f"Consultas com erro: {len(errors)}")
    print(f"Palavras na referência: {total_references}")
    print(f"Total de erros: {total_errors}")
    print(f"WER global: {global_wer:.2%}")
    print(f"CSV gerado: {CSV_FILE}")

    if errors:
        print("\nConsultas que apresentaram erros:")

        for error in errors:
            print(f"{error['consulta']}: {error['erro']}")


if __name__ == "__main__":
    processar_consultas()
