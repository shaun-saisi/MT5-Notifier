import MetaTrader5 as mt5
import pandas as pd

# Replace with YOUR Deriv demo MT5 credentials
ACCOUNT = 12345678          # your MT5 account number
PASSWORD = "your_password"
SERVER = "Deriv-Demo"       # exact server name from MT5 login dialog

if not mt5.initialize(login=ACCOUNT, password=PASSWORD, server=SERVER):
    print("initialize failed:", mt5.last_error())
    quit()

print("Connected:", mt5.account_info().login)
print("Balance:", mt5.account_info().balance)

# Fetch 10 daily EURUSD candles
rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_D1, 0, 10)
if rates is None or len(rates) == 0:
    print("No data. Symbol may not be visible in MarketWatch.")
    print("Error:", mt5.last_error())
else:
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    print(df[['time', 'open', 'high', 'low', 'close']])

mt5.shutdown()