"""
Stage 1 diagnostic: Verify Python can attach to the running MT5 terminal.
Run: python test_mt5.py
"""

import MetaTrader5 as mt5

if not mt5.initialize():
    print("initialize failed:", mt5.last_error())
    quit()

info = mt5.account_info()
print("login:", info.login)
print("server:", info.server)
print("balance:", info.balance)

rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_D1, 0, 5)
if rates is None or len(rates) == 0:
    print("No EURUSD data. Fix: MT5 Market Watch -> Show All")
    print("Error:", mt5.last_error())
else:
    print(f"Fetched {len(rates)} candles. First candle:")
    print(rates[0])

mt5.shutdown()