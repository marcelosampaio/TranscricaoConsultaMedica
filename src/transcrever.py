from pathlib import Path

import torch
import whisper


DATASET_DIR = (
    Path.home()
    / "PythonFolder"
    / "TranscricaoConsultaMedicaDataSets"
)

AUDIO_FILE = DATASET_DIR / "audios_fornecidos" / "CAR0001.mp3"


def carregar_modelo(model_name="base"):
    device = "mps" if torch.backends.mps.is_available() else "cpu"

    print(f"Dispositivo: {device}")
    print(f"Carregando modelo Whisper {model_name}...")

    return whisper.load_model(model_name, device=device)


def transcrever_audio(audio_file, model):
    audio_file = Path(audio_file)

    if not audio_file.is_file():
        raise FileNotFoundError(f"Áudio não encontrado: {audio_file}")

    result = model.transcribe(
        str(audio_file),
        language="en",
        fp16=False,
    )

    return result["text"].strip()


def main():
    model = carregar_modelo()

    print("Iniciando transcrição de CAR0001...")

    transcription = transcrever_audio(AUDIO_FILE, model)

    print("\nTexto reconhecido:")
    print(transcription)


if __name__ == "__main__":
    main()
