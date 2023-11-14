
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
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

def black_scholes_put(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return put_price

def implied_volatility(option_price, S, K, T, r, cop:bool=True):
    # Define the objective function to find the root (i.e., implied volatility)
    def objective_function(sigma):
        return black_scholes_call(S, K, T, r, sigma) - option_price

    def put_function(sigma):
        return black_scholes_put(S, K, T, r, sigma) - option_price

    # Use bisect method to find the root within a specified range
    try:
        if(cop):
            implied_vol = bisect(objective_function, 0.001, 2)
            return implied_vol
        else:
            return bisect(put_function, 0.001,2)
    except ValueError as e:
        return 0.000001


def calculate_leverage(notional_value, option_price):
    return notional_value / option_price


if __name__ ==  "__main__":
    # Example usage:
    option_price = 0.0029  # Replace with the actual market option price
    current_asset_price = 3.65  # Replace with the current asset price
    strike_price = 3.3 # Replace with the option's strike price
    time_to_maturity = 43/365  # Replace with the time to maturity in years
    risk_free_rate = 0.0245  # Replace with the risk-free interest rate
    implied_volatility_value = implied_volatility(option_price, current_asset_price, strike_price, time_to_maturity,
                                                  risk_free_rate,False)
    print("Implied Volatility:", implied_volatility_value)
    print(black_scholes_call(current_asset_price, strike_price, time_to_maturity, risk_free_rate, 0.00001)
          - option_price)

