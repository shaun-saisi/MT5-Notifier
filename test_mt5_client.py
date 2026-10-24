"""
Smoke test for mt5_client.fetch_multi_timeframe.
"""

import mt5_client
import config

mt5_client.connect()

for symbol in config.SYMBOLS:
    try:
        data = mt5_client.fetch_multi_timeframe(symbol)
        counts = {k: len(v) for k, v in data.items()}
        print(f"{symbol}: {counts}")
    except Exception as e:
        print(f"{symbol}: FAILED - {e}")

mt5_client.disconnect()