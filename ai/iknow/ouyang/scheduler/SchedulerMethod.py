import datetime
import os

import requests

from properties import bao_time_format, tushare_time_format, job_times
from utils.stockUtil import call_BSM, put_BSM
import pandas as pd


path = "result"
if(not os.path.exists(path)): os.makedirs(path)
def test(param1):
    print(param1)


def getBSM():
    print("getBSM start")
    today = datetime.datetime.now().strftime(tushare_time_format)
    job_times["getBSM%s" % today] = -1
    days = 250 # 股票一年的开市时间
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
            index +=1
            job_times["getBSM%s" % today] = round(index/job_len*100,2)
        df = pd.DataFrame.from_dict(datas)
        df.to_csv("%s%s%s%s.csv" % (path,os.sep,"option_last_", today),encoding="utf-8")
        job_times["getBSM%s" % today] = 100
        print("getBSM END")

if(__name__ == "__main__"):
    getBSM()
    datas = {
        "price": []
    }
    datas["price"].append("%.6f" % 0.000001)
    df = pd.DataFrame().from_dict(datas)
    df["price"].astype(str)
    df.to_csv("test.csv")
