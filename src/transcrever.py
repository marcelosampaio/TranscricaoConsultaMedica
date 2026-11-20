from pathlib import Path

import torch
import whisper


DATASET_DIR = (
    Path.home()
    / "PythonFolder"
    / "TranscricaoConsultaMedicaDataSets"
)

AUDIO_FILE = DATASET_DIR / "audios_fornecidos" / "CAR0001.mp3"

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
OUTPUT_FILE = RESULTS_DIR / "CAR0001_whisper_base.txt"


def main():
    if not AUDIO_FILE.is_file():
        raise FileNotFoundError(f"Áudio não encontrado: {AUDIO_FILE}")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    device = "mps" if torch.backends.mps.is_available() else "cpu"

    print(f"Dispositivo: {device}")
    print("Carregando modelo Whisper base...")

    model = whisper.load_model("base", device=device)

    print("Iniciando transcrição de CAR0001...")

    result = model.transcribe(
        str(AUDIO_FILE),
        language="en",
        fp16=False,
    )

    transcription = result["text"].strip()

    OUTPUT_FILE.write_text(transcription + "\n", encoding="utf-8")

    print(f"\nTranscrição salva em: {OUTPUT_FILE}")
    print("\nTexto reconhecido:")
    print(transcription)


if __name__ == "__main__":
    main()
