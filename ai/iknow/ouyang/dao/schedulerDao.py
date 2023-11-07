from dbconnection.mongoConnection import mongo_conn
from properties import scheduler_col, tmp_scheduler_col


class SchedulerDao():
    """
        用于保存计划任务的collection
    {
        'id': 'test', # id 必须唯一
        "name": "scheduler_factory.test", # name需要有标识性
        'func': "scheduler.SchedulerServer:scheduler_factory.test", # 触发方法
        'trigger': "interval", # 触发频率
        'seconds': 60
    }
    {
        'id': 'test', # id 必须唯一
        "name": "scheduler_factory.test", # name需要有标识性
        'func': "scheduler.SchedulerServer:scheduler_factory.test", # 触发方法
        'trigger': {
            'type': 'cron', # 触发频率
            'hour': 5,
            'minute': 50
        }
        'seconds': 60
    }
    """

    def __init__(self):
        self.__scheduler_col = mongo_conn[scheduler_col]
        self.__tmp_scheduler_col = mongo_conn[tmp_scheduler_col]

    def get_all(self):
        return list(self.__scheduler_col.find())

    def upsert_tmp_scheduler(self, scheduler_info):
        scheduler_info["_id"] = scheduler_info["id"]
        self.__tmp_scheduler_col.update({"_id": scheduler_info["_id"]}, {"$set": scheduler_info}, upsert=True)


# scheduler_dao = SchedulerDao()
