"""
Central configuration.
Loads secrets from .env; all tunable values live here.
"""

import os
from dotenv import load_dotenv

# Load variables from .env into the environment
load_dotenv()

# --- Deriv authentication ---
DERIV_API_TOKEN = os.environ.get("DERIV_API_TOKEN", "")

if not DERIV_API_TOKEN:
    raise RuntimeError(
        "DERIV_API_TOKEN is missing. "
        "Create a .env file in the project root with:\n"
        "DERIV_API_TOKEN=your_token_here"
    )

# --- Deriv market settings ---
SYMBOL = "R_100"            # Deriv symbol (R_10, R_25, R_75, R_100, etc.)
CANDLE_COUNT = 10           # Number of candles to fetch
GRANULARITY = 3600          # Seconds per candle (60=1min, 3600=1h, 14400=4h)
DERIV_APP_ID = "1089"       # Deriv public test app_id (fine for read-only)

# --- Ollama (local LLM) settings ---
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"     # Must be pulled with: ollama pull llama3
OLLAMA_TIMEOUT = 120        # Seconds before giving up on a request