"""Web loader: fetches a URL and returns text."""
import requests


def load_url(url: str) -> str:
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.text
