"""
Central configuration.
Phase 1-3 uses only public market data, so no token is required.
Token will be needed later (Phase 4) when we place orders.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- Deriv authentication (not needed for Phase 1-3, kept for later) ---
DERIV_API_TOKEN = os.environ.get("DERIV_API_TOKEN", "")

# --- Deriv market settings ---
SYMBOL = "R_100"            # Deriv symbol (R_10, R_25, R_75, R_100, etc.)
CANDLE_COUNT = 10           # Number of candles to fetch
GRANULARITY = 3600          # Seconds per candle (60=1min, 3600=1h, 14400=4h)

# --- Ollama (local LLM) settings ---
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"     # Must be pulled with: ollama pull llama3
OLLAMA_TIMEOUT = 120        # Seconds before giving up on a request