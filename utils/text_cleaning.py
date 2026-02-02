"""Minimal text cleaning utilities."""
import re


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\s+", " ", text)
    return text.strip()
