import asyncio
from deriv_api import DerivAPI

async def main():
    api = DerivAPI(app_id=1089)
    try:
        response = await api.ping({'ping': 1})
        print("Connection OK:", response)
    except Exception as e:
        print("Connection failed:", type(e).__name__, str(e))
    finally:
        await api.clear()

asyncio.run(main())