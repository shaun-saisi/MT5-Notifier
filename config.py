"""
Central configuration for MT5 forex AI agent.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- MT5 connection ---
# Terminal already logged in (5057833335, MetaQuotes-Demo). No credentials here.

# --- Top five forex pairs by volume ---
SYMBOLS = ["EURUSD", "USDJPY", "GBPUSD", "USDCAD", "AUDUSD"]

# --- Timeframes ---
CANDLE_COUNT = 20

# --- AI scoring threshold ---
MIN_SCORE = 70

# --- Liquidity window (Kenya time, EAT, UTC+3) ---
LIQUIDITY_START_HOUR = 16
LIQUIDITY_END_HOUR = 20

# --- Position sizing ---
LOT_SIZE = 0.01

# --- Holding period ---
MIN_HOLD_DAYS = 3

# --- Ollama settings ---
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:1b"    # smaller, faster; switch back to "llama3" if you have a strong GPU
OLLAMA_TIMEOUT = 600