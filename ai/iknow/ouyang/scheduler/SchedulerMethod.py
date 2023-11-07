import datetime

import requests

from properties import bao_time_format
from utils.stockUtil import call_BSM, put_BSM
import pandas as pd


def test(param1):
    print(param1)


def getBSM():
    days = 250 # 股票一年的开市时间
    res = requests.get("https://api.sdqtrade.com/data/option/latest/sh000300")
    if(res.status_code == 200):
        body = res.json()
        results = body.get("results")
        datas = {
            "symbol": [],
            "name": [],
            "bsm_price": [],
            "underlyingPrice": [],
            "strike": [],
            "sigma": [],
            "expirationDate": []
        }
        start_day = datetime.datetime.strptime(datetime.datetime.now().strftime(bao_time_format), bao_time_format)
        for each in results:
            end_day = datetime.datetime.strptime(each["expirationDate"], bao_time_format)
            dela = (end_day - start_day).days
            if(each["type"] == "C"):
                result:float = call_BSM(each["underlyingPrice"], each["strike"], 0, each["sigma"]*days, 0.02, dela/365)
            else:
                result: float = put_BSM(each["underlyingPrice"], each["strike"], 0, each["sigma"] * days, 0.02,
                                         dela / 365)
            datas["symbol"].append(each["symbol"])
            datas["name"].append(each["name"])
            datas["underlyingPrice"].append(each["underlyingPrice"])
            datas["strike"].append(each["strike"])
            datas["sigma"].append(each["sigma"])
            datas["expirationDate"].append(each["expirationDate"])
            datas["bsm_price"].append(round(result, 4))
        df = pd.DataFrame.from_dict(datas)
        df.to_csv("result.csv",encoding="utf-8")

if(__name__ == "__main__"):
    getBSM()
    # each = {"symbol":"90002159","name":"中证500ETF购12月5250","strike":5.2500,"type":"C",
    #         "underlyingSecurity":"159922","underlyingPrice":5.821,"month":202312,"expirationDate":"2023-12-27",
    #         "period":"month","lastPrice":0.5219,"volume":2,"openInterest":753,"sigma":0.000595,
    #         "closeTime":1699236600000}
    # start_day = datetime.datetime.strptime(datetime.datetime.now().strftime(bao_time_format), bao_time_format)
    # end_day = datetime.datetime.strptime(each["expirationDate"], bao_time_format)
    # days = 250
    # dela = (end_day - start_day).days
    # print(0.1488 / 250)
    # result: float = call_BSM(each["underlyingPrice"], each["strike"], 0, each["sigma"] * days, 0.02438, dela / 365)
    # print(result)