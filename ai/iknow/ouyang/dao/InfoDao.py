import datetime
from threading import Thread
from traceback import print_exc

from dbconnection.mongoConnection import mongo_conn
from properties import minute_format
from utils.AppUtil import generate_token





class InfoDao():

    def __init__(self):
        self.mon_conn = mongo_conn
        self.cols = {}


    def insert_az_infos(self,infos,az="HK"):
        col = self.get_az_col(az)
        today = datetime.datetime.now().strftime(minute_format)
        for each in infos:
            if(each.get("create_time") is None):
                each["create_time"] = today
            each["_id"] = generate_token(each["symbol"]+ each["create_time"])
        col.insert_many(infos)

    def get_az_col(self,az):
        key = "info%s" % az
        col = self.cols.get(key)
        if(col is None):
            col = self.mon_conn[key]
        self.cols[key] = col
        return col
    '''
        数据单条处理非批量
    '''
    def insert_infos(self,infos):
        now = None
        print("insert_start")
        for each in infos:
            if(each.get("create_time") is None):
                if(now is None):
                    now = datetime.datetime.now().strftime(minute_format)
                each["create_time"] = now
            symbol = each["symbol"]
            col = self.get_col(symbol)
            if(col is None):
                continue
            each["_id"] = generate_token(each["symbol"],each["create_time"])
            try:
                col.insert_one(each)
            except Exception as e:
                print_exc()
        print("insert_complete")

    def get_col(self,symbol):
        key = self.get_key(symbol)
        if(key is None): return None
        col = self.cols.get(key)
        if(col is None):
            col = self.add_col(symbol)
        return col
    def add_col(self,symbol):
        key = self.get_key(symbol)
        if(key is None): return key
        col = self.mon_conn[key]
        self.cols[key] = col
        return col

    def get_key(self,symbol):
        if (symbol is None or symbol == ""): return None
        return "info%s" % symbol
def insert_result(dao:InfoDao,infos):
    dao.insert_infos(infos)

info_dao = InfoDao()
def async_insert(infos):
    t = Thread(target=insert_result,args=(info_dao,infos))
    t.start()

