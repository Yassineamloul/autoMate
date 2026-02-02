"""Ingestion agent with simple retry logic."""
import time
from typing import Callable


def retry(fn: Callable, retries: int = 3, delay: float = 1.0):
    for attempt in range(1, retries + 1):
        try:
            return fn()
        except Exception as e:
            if attempt == retries:
                raise
            time.sleep(delay)


def ingest_document(loader_fn, *args, **kwargs):
    """Call a loader function with retries and return text."""

    def _call():
        return loader_fn(*args, **kwargs)

    return retry(_call)
