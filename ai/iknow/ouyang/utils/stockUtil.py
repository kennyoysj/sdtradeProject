import datetime
import math
import time
from threading import Thread

import requests

from properties import bao_time_format


def call_BSM(S,K,V,sigma,r,T):
    '''BSM模型计算看涨期权的价格
    S:期权基础资产的价格；
    K：期权的执行价格；
    V:支付红利的现值;
    sigma:基础资产价格百分比变化的年化波动率；
    r:无风险收益率；
    T：期权合约的剩余期限；'''
    import numpy as np
    from scipy.stats import norm
    d1=(np.log((S-V)/K)+(r+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2=d1-sigma*np.sqrt(T)
    return (S-V)*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)

def put_BSM(S,K,V,sigma,r,T):
    '''BSM模型计算看跌期权的价格
    S:期权基础资产的价格；
    K：期权的执行价格；
    V:支付红利的现值;
    sigma:基础资产价格百分比变化的年化波动率；
    r:无风险收益率；
    T：期权合约的剩余期限；'''
    import numpy as np
    from scipy.stats import norm
    d1=(np.log((S-V)/K)+(r+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2=d1-sigma*np.sqrt(T)
    return K*np.exp(-r*T)*norm.cdf(-d2)-(S-V)*norm.cdf(-d1)

from scipy.stats import norm
from scipy.optimize import bisect
import numpy as np
def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    nd1 = norm.cdf(d1)
    nd2 = norm.cdf(d2)
    call_price = S * nd1 - K * np.exp(-r * T) * nd2
    return call_price

def black_scholes_put(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return put_price

def implied_volatility(option_price, S, K, T, r, cop:bool=True):
    # Define the objective function to find the root (i.e., implied volatility)
    def call_function(sigma):
        return black_scholes_call(S, K, T, r, sigma) - option_price

    def put_function(sigma):
        return black_scholes_put(S, K, T, r, sigma) - option_price

    # Use bisect method to find the root within a specified range
    try:
        if(cop):
            implied_vol = bisect(call_function, 0.0001, 2)
            return implied_vol
        else:
            return bisect(put_function, 0.0001, 2)
    except ValueError as e:
        return 0.000001


def calculate_leverage(notional_value, option_price):
    return notional_value / option_price


def calculate_delta(S, K, T, r, sigma, call_or_put):
    if(T<0): return 1
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    if call_or_put == "C":
        delta = norm.cdf(d1)
    elif call_or_put == "P":
        delta = norm.cdf(d1) - 1
    else:
        raise ValueError("Invalid option type. Use 'C' or 'P'.")
    return delta

risk_free_dic = {

}
def get_risk_free_rate(az="HK"):
    """
        这里获取的是三个月的无风险利率
    """

    now = datetime.datetime.now()
    weekday = now.weekday()
    if(weekday >= 5):
        now -= datetime.timedelta(days=(weekday-4))
    rf_dic = risk_free_dic.get(az, {})
    if(az == "HK"):
        res = None
        retry=0
        while(res == None and retry<5):
            key = now.strftime(bao_time_format)
            rf = rf_dic.get(key)
            if(rf != None and rf != -100):
                risk_free_dic[az] = rf_dic
                return rf
            elif(rf == -100):
                now -= datetime.timedelta(days=1)
                continue
            res = requests.get("https://www.hkab.org.hk/api/hibor?year=%d&month=%d&day=%d" % (now.year,now.month,now.day))
            if(res.status_code == 200):
                jdata = res.json()
                rf = jdata.get("3 Months")
                if(rf == None):
                    res = None
                    rf_dic[key] = -100
                    now -= datetime.timedelta(days=1)
                else:
                    risk_free_dic[az] = rf_dic
                    return rf
            else:
                res = None
                retry += 1
                time.sleep(10)
        return 5.6
    elif(az == "CN"):
        res = None
        retry = 0
        while (res == None and retry < 5):
            key = now.strftime(bao_time_format)
            rf = rf_dic.get(key)
            if (rf != None and rf != -100):
                risk_free_dic[az] = rf_dic
                return rf
            elif (rf == -100):
                now -= datetime.timedelta(days=1)
                continue
            res = requests.post("https://www.shibor.org/r/cms/www/chinamoney/data/shibor/shibor.json", data={})
            if (res.status_code == 200):
                jdata = res.json()
                records = jdata.get("records")
                for each in records:
                    if(each.get("termCode") == "3M"):
                        rf_dic[key] = each.get("shibor")
                        risk_free_dic[az] = rf_dic
                        return rf_dic[key]
            else:
                res = None
                retry += 1
                time.sleep(10)
        return 2.46

if __name__ ==  "__main__":
    print(get_risk_free_rate("HK"))
    print(get_risk_free_rate("CN"))
    # Example usage:
    # option_price = 0.0029  # Replace with the actual market option price
    # current_asset_price = 3.65  # Replace with the current asset price
    # strike_price = 3.3 # Replace with the option's strike price
    # time_to_maturity = 43/365  # Replace with the time to maturity in years
    # risk_free_rate = 0.0245  # Replace with the risk-free interest rate
    # implied_volatility_value = implied_volatility(option_price, current_asset_price, strike_price, time_to_maturity,
    #                                               risk_free_rate,True)
    # print("Implied Volatility:", implied_volatility_value)
    # print(black_scholes_call(current_asset_price, strike_price, time_to_maturity, risk_free_rate, 0.00001)
    #       - option_price)
    print(calculate_delta(3.605,3.400,61/365,0.024620,0.1213,"C"))
    print(0.76363/100 * np.sqrt(252))

