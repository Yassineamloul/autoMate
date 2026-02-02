"""Configuration and secrets for local demo.
Set environment variables to override defaults in production.
"""
import os

# Model / API keys (placeholders)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# Index settings
INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "outputs", "index.db")
