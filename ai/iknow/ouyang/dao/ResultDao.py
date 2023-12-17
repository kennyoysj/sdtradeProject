import pymongo

from dbconnection.mongoConnection import mongo_conn


class ResultDao():

    def __init__(self):
        self.mon_conn = mongo_conn


    def insertResult(self,datas:list,az):
        if(datas == []): return
        col = self.mon_conn[az]
        # ids = [x["_id"] for x in datas]
        # res = col.find({"_id":{"$in": ids}})
        # inIds = [x["_id"] for x in res]
        # inserts = []
        # for each in datas:
        #     if(each not in inIds):
        #         inserts.append(each)
        col.insert_many(datas,ordered=False)

    def getResult(self, az:str, symbol, limit = 1000):
        az = az.upper()
        col = self.mon_conn[az]
        res = list(col.find({"symbol":symbol}).sort([("create_time", pymongo.DESCENDING)]).limit(limit))
        return res

res_dao = ResultDao()