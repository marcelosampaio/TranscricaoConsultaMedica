
import re
import string
from pathlib import Path

from jiwer import process_words


DATASET_DIR = (
    Path.home()
    / "PythonFolder"
    / "TranscricaoConsultaMedicaDataSets"
)

REFERENCE_FILE = (
    DATASET_DIR
    / "transcricoes_fornecidas"
    / "CAR0001.txt"
)

HYPOTHESIS_FILE = (
    Path(__file__).resolve().parent.parent
    / "results"
    / "CAR0001_whisper_base.txt"
)


def load_transcription(file_path):
    if not file_path.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    return file_path.read_text(encoding="utf-8")


def normalize_reference(text):
    text = re.sub(r"(?m)^[DP]:\s*", "", text)
    return normalize_text(text)


def normalize_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return " ".join(text.split())


def main():
    reference = load_transcription(REFERENCE_FILE)
    hypothesis = load_transcription(HYPOTHESIS_FILE)

    reference = normalize_reference(reference)
    hypothesis = normalize_text(hypothesis)

    result = process_words(reference, hypothesis)

    print("Avaliação da transcrição CAR0001")
    print("--------------------------------")
    print(f"Palavras na referência: {result.hits + result.substitutions + result.deletions}")
    print(f"Palavras no Whisper: {len(hypothesis.split())}")
    print(f"Correspondências corretas: {result.hits}")
    print(f"Substituições (S): {result.substitutions}")
    print(f"Exclusões (D): {result.deletions}")
    print(f"Inserções (I): {result.insertions}")
    print(f"Word Error Rate (WER): {result.wer:.2%}")


if __name__ == "__main__":
    main()
