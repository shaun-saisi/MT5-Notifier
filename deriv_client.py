"""
Deriv data layer. Fetches candles from Deriv's WebSocket API.
"""

from deriv_sdk import DerivClient
import config


async def fetch_candles():
    """
    Connect to Deriv (authenticated), fetch recent candles.
    Returns a list of candle dicts.
    Raises RuntimeError if no data is returned.
    """
    print(f"[Deriv] Fetching {config.CANDLE_COUNT} candles for {config.SYMBOL}...")

    client = DerivClient(
        app_id=config.DERIV_APP_ID,
        api_token=config.DERIV_API_TOKEN,
    )
    await client.start()

    candles = await client.market.ticks_history(
        config.SYMBOL,
        count=config.CANDLE_COUNT,
        granularity=config.GRANULARITY,
        style="candles",
    )

    await client.close()

    if not candles:
        raise RuntimeError("Deriv returned empty candle data.")

    print(f"[Deriv] Received {len(candles)} candles.")
    return candles