import pymongo

from dbconnection.mongoConnection import mongo_conn


class ResultDao():

    def __init__(self):
        self.mon_conn = mongo_conn


    def insertResult(self,datas,az):
        if(datas == []): return
        col = self.mon_conn[az]
        col.insert_many(datas)

    def getResult(self, az:str, symbol, limit = 1000):
        az = az.upper()
        col = self.mon_conn[az]
        res = list(col.find({"symbol":symbol}).sort([("create_time", pymongo.DESCENDING)]).limit(limit))
        return res

res_dao = ResultDao()