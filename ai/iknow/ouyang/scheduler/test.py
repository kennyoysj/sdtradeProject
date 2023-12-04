import datetime

from properties import bao_time_format
from utils.stockUtil import implied_volatility, calculate_delta

each = {'symbol': 'HHI231201P5800000', 'name': None, 'strike': 5800, 'type': 'P', 'underlyingSecurity': 'HHIW', 'underlyingPrice': 16651.01, 'month': 202312, 'expirationDate': '2023-12-01', 'period': 'week', 'lastPrice': 1.0, 'volume': 0, 'openInterest': 1042, 'sigma': 136.09221, 'closeTime': 1701698640000}
key: str = each["symbol"]
free_rate = 0.0246
start_day = datetime.datetime.strptime(datetime.datetime.now().strftime(bao_time_format), bao_time_format)
end_day = datetime.datetime.strptime(each["expirationDate"], bao_time_format)
dela = (end_day - start_day).days
option_price = each["lastPrice"]  # Replace with the actual market option price
current_asset_price = each["underlyingPrice"]  # Replace with the current asset price
strike_price = each["strike"]  # Replace with the option's strike price
time_to_maturity = dela / 365  # Replace with the time to maturity in years
if(each["type"] == 'C'): # call action
    vol = implied_volatility(option_price, current_asset_price, strike_price, time_to_maturity,
                             free_rate)
else:
    vol = implied_volatility(option_price, current_asset_price, strike_price, time_to_maturity,
                             free_rate, False)
if (vol < 0.001 and vol > 0.00001):
    print(each)
delta = calculate_delta(current_asset_price, strike_price, time_to_maturity, free_rate,dela,each["type"])
if (option_price == 0):
    leverage = 0
else:
    leverage = current_asset_price / option_price
actual_leverage = leverage*delta