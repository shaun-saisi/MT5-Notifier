"""
Deriv data layer. Fetches candles from Deriv's public WebSocket API.
No authentication required for market data (Phase 1-3).
"""

import asyncio
import json

import websockets

import config


PUBLIC_WS_URL = "wss://api.derivws.com/trading/v1/options/ws/public"


async def fetch_candles():
    """
    Connect to Deriv's public WebSocket, request recent candles,
    return the candle list. Raises RuntimeError on bad responses.
    """
    print(f"[Deriv] Fetching {config.CANDLE_COUNT} candles for {config.SYMBOL}...")

    request = {
        "ticks_history": config.SYMBOL,
        "count": config.CANDLE_COUNT,
        "granularity": config.GRANULARITY,
        "style": "candles",
        "end": "latest",
    }

    try:
        async with websockets.connect(PUBLIC_WS_URL, open_timeout=15) as ws:
            await ws.send(json.dumps(request))
            raw = await asyncio.wait_for(ws.recv(), timeout=20)
    except (OSError, websockets.exceptions.WebSocketException) as e:
        raise RuntimeError(
            f"Could not connect to Deriv public WebSocket: {e}\n"
            f"URL tried: {PUBLIC_WS_URL}\n"
            "Check your internet connection or try a different network."
        ) from e
    except asyncio.TimeoutError as e:
        raise RuntimeError(
            "Deriv WebSocket timed out while waiting for a response."
        ) from e

    try:
        response = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Deriv returned non-JSON response: {raw[:200]}") from e

    if "error" in response:
        raise RuntimeError(
            f"Deriv API error: {response['error'].get('message', 'unknown')}"
        )

    candles = response.get("candles")
    if not candles:
        raise RuntimeError(f"Deriv returned no candles. Full response: {response}")

    print(f"[Deriv] Received {len(candles)} candles.")
    return candles