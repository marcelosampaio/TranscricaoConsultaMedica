import re
import string

from jiwer import process_words


def normalizar_referencia(text):
    text = re.sub(r"(?m)^[DP]:\s*", "", text)
    return normalizar_texto(text)


def normalizar_texto(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return " ".join(text.split())


def avaliar_transcricao(reference, hypothesis):
    reference = normalizar_referencia(reference)
    hypothesis = normalizar_texto(hypothesis)

    result = process_words(reference, hypothesis)

    return {
        "palavras_referencia": result.hits + result.substitutions + result.deletions,
        "palavras_whisper": len(hypothesis.split()),
        "hits": result.hits,
        "substitutions": result.substitutions,
        "deletions": result.deletions,
        "insertions": result.insertions,
        "wer": result.wer,
    }
