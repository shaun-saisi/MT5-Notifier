"""
Prompt construction layer. Turns candle data into a prompt string.
"""

import json
import config


def build_prompt(candles) -> str:
    return f"""
You are a conservative swing trader analyzing the {config.SYMBOL} market.

Below are the most recent {len(candles)} one-hour candles (JSON):
{json.dumps(candles, indent=2)}

Based ONLY on this data, give a brief trading plan:
1. Market bias (Bullish / Bearish / Neutral) and the structural reason.
2. Suggested entry range.
3. Stop-loss level.
4. Take-profit target (at least 1:2 risk-reward).

Keep it short. Do not invent data that is not present above.
"""