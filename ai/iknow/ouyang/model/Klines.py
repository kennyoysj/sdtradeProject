import json
from datetime import datetime

from dbconnection.redisConnection import redis_conn
from model.Kline import Kline


class Klines():

    def __init__(self):
        self.code = None
        self.freq = None
        self.data = []

    # 从redis 里面获取数据并填充
    def init_klines(self, code, freq):
        result = redis_conn.get("{0}_{1}".format(code, freq))
        if(result is None or result == ""):
            return None
        else:
            result = json.loads(result)
            datas = result.get("data")
            data_list = []
            for each in datas:
                kline = Kline()
                kline.set_dict(each)
                data_list.append(kline)
            self.data = data_list
            self.code = code
            self.freq = freq

    # 更新redis数据 此方法的调用必须初始化调用 init_klines
    def update_klines(self, kline:Kline):
        last_kline = self.data[-1] # type:Kline
        flag = False
        time1 = datetime.strptime(last_kline.date_time, "%Y%m%d %H:%M:%S")
        time2 = datetime.strptime(kline.date_time, "%Y%m%d %H:%M:%S")
        if(time1 < time2): # 时间大于的话增加一位
            self.data.append(kline)
            flag = True
        elif(time1 == time2): # 时间相同则更新
            self.data[-1] = kline
        if(len(self.data) > 20): # 超过20条数据则删除最早的一条
            self.data.pop(0)
        redis_conn.set("{0}_{1}".format(self.code, self.freq), json.dumps(self.get_dict()))
        return flag

    # 从kline接口获取的初始化服务器数据
    def reset_kilnes(self, code, freq, datas):
        self.code = code
        self.freq = freq
        self.data = []
        for each in datas:
            kline = Kline()
            kline.set_dict(each)
            self.data.append(kline)
        redis_conn.set("{0}_{1}".format(code, freq), json.dumps(self.get_dict()))


    # 将获取的数据转为dict
    def get_dict(self):
        data = {
            "freq": self.freq,
            "code": self.code,
            "data": []
        }
        for each in self.data: # type: Kline
            data["data"].append(each.get_dict())
        return data