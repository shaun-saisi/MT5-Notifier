"""
Prompt construction for multi-timeframe AI scoring.
Returns a JSON-only response from the AI, no markdown.
"""

import json


def build_scoring_prompt(symbol, mtf_data):
    """
    Build a prompt that asks the AI to score a setup from 0-100
    using Daily (trend), H4 (zone), and H1 (entry).
    """
    return f"""
You are a 20-year forex swing trader. Analyze {symbol} using three timeframes.
Daily = overall trend direction. H4 = support/resistance zone. H1 = entry timing.

DAILY candles (oldest to newest):
{json.dumps(mtf_data['daily'], indent=1)}

H4 candles (oldest to newest):
{json.dumps(mtf_data['h4'], indent=1)}

H1 candles (oldest to newest):
{json.dumps(mtf_data['h1'], indent=1)}

Score this setup from 0 to 100 using these weighted criteria:
- Daily trend alignment with your direction: 0-30 points
- H4 price is near a clear support (for BUY) or resistance (for SELL): 0-25 points
- H1 candle confirms entry (reversal or continuation): 0-25 points
- Stop-loss and take-profit give at least 1:2 risk-reward: 0-20 points

Rules:
- If the trend is unclear or the setup is weak, set direction to "NONE" and score to 0.
- Use ONLY prices from the data above. Do not invent numbers.
- Return ONLY valid JSON. No markdown, no code fences, no explanation.

JSON format:
{{
  "symbol": "{symbol}",
  "direction": "BUY" or "SELL" or "NONE",
  "score": 0,
  "entry": 0.0,
  "sl": 0.0,
  "tp": 0.0,
  "reason": "one sentence"
}}
"""