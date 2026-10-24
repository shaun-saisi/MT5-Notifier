"""
MT5 data layer. Fetches multi-timeframe candles for any symbol.
"""

import MetaTrader5 as mt5
import pandas as pd
import config


def connect():
    """Attach Python to the running MT5 terminal."""
    if not mt5.initialize():
        raise RuntimeError(f"MT5 initialize failed: {mt5.last_error()}")


def disconnect():
    """Cleanly close the connection."""
    mt5.shutdown()


def fetch_multi_timeframe(symbol):
    """
    Returns dict: {'daily': [...], 'h4': [...], 'h1': [...]}
    Each list contains OHLC dicts sorted oldest-to-newest.
    """
    timeframes = {
        "daily": mt5.TIMEFRAME_D1,
        "h4": mt5.TIMEFRAME_H4,
        "h1": mt5.TIMEFRAME_H1,
    }

    if not mt5.symbol_select(symbol, True):
        raise RuntimeError(f"Could not select symbol {symbol}")

    result = {}
    for name, tf in timeframes.items():
        rates = mt5.copy_rates_from_pos(symbol, tf, 0, config.CANDLE_COUNT)
        if rates is None or len(rates) == 0:
            raise RuntimeError(f"No {name} data for {symbol}: {mt5.last_error()}")

        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s").astype(str)
        result[name] = df[["time", "open", "high", "low", "close"]].to_dict("records")

    return result