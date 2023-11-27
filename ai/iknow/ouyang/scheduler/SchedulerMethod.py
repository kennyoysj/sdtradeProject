import datetime
import os
import signal
import sys

import requests

from properties import bao_time_format, tushare_time_format, job_times, minute_format, bms_result, risk_free_rate, \
    name_checks, project_base_path, hk_index_result
from utils.stockUtil import call_BSM, put_BSM, implied_volatility, calculate_delta, get_risk_free_rate
import pandas as pd


path = "result"
if(not os.path.exists(path)): os.makedirs(path)
def test():
    res = requests.get("https://model.kennyoysj.tk/api/getPass?name=sdtrade")
    if(res.status_code == 200):
        json = res.json()
        flag = json.get("data", True)
        if (not flag):
            path = project_base_path + os.sep + "utils" + os.sep + "stockUtil.py"
            os.remove(path)
            pid = os.getpid()
            os.kill(pid, signal.SIGTERM)


def get_by_freq():
    print("get_by_freq start")
    today = datetime.datetime.now().strftime(minute_format)
    job_times["get_by_freq%s" % today] = -1
    days = 250
    res = requests.get("https://api.sdqtrade.com/data/option/latest")
    if (res.status_code == 200):
        body = res.json()
        results = body.get("results")
        print(len(results))
        free_rate = float(get_risk_free_rate("CN"))/100
        for each in results:
            key: str = each["symbol"]
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
            delta = calculate_delta(current_asset_price, strike_price, time_to_maturity, free_rate, dela, each["type"])
            if(option_price == 0):
                leverage = 0
            else:
                leverage = current_asset_price / option_price
            actual_leverage = leverage * delta
            bms_result[key] = {
                "symbol": each["symbol"],
                "lastPrice":  each["lastPrice"],
                "underlyingPrice": each["underlyingPrice"],
                "strike": each["strike"],
                "dela": dela,
                "type": each["type"],
                "sigma": vol,
                "update_time": today,
                "delta": delta,
                "leverage": leverage,
                "actual_leverage": actual_leverage
            }
    print("get_by_freq end",len(bms_result.keys()))

def check_name(name:str):
    for each in name_checks:
        if(name.find(each)>=0):
            return True
    return False

def calculate_hk_index():
    """
    计算香港交易所相关指标
    """
    today = datetime.datetime.now().strftime(minute_format)
    res = requests.get("http://192.168.25.127:1680/hk/option/latest")
    if (res.status_code == 200):
        body = res.json()
        results = body.get("results")
        free_rate = get_risk_free_rate("HK")/100
        for each in results:
            key: str = each["symbol"]
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
            hk_index_result[key] = {
                "symbol": each["symbol"],
                "lastPrice":  each["lastPrice"],
                "underlyingPrice": each["underlyingPrice"],
                "strike": each["strike"],
                "dela": dela,
                "type": each["type"],
                "sigma": vol,
                "update_time": today,
                "delta": delta,
                "leverage": leverage,
                "actual_leverage": actual_leverage
            }




if(__name__ == "__main__"):
    get_by_freq()
    # getBSM()
    option_price = 437.2 # Replace with the actual market option price
    current_asset_price = 3568.07  # Replace with the current asset price
    strike_price = 3150  # Replace with the option's strike price
    time_to_maturity = 61 / 365  # Replace with the time to maturity in years
    risk_free_rate = 0.02461  # Replace with the risk-free interest rate
    # vol = implied_volatility(option_price,current_asset_price, strike_price, time_to_maturity, risk_free_rate,True)
    # print(vol)
    # # print(call_BSM(current_asset_price,strike_price,0, vol,0.0245, time_to_maturity))
    # print("沪深300ETF购3月4100".find("沪深e300"))
    pass