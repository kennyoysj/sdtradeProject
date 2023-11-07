
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