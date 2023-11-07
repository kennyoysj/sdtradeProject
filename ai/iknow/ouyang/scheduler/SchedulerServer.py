# encoding:utf-8
from apscheduler.job import Job

from scheduler.Scheduler import scheduler

class SchedulerFactory:
    """
        这里主要保存一些日常定时任务,为防止出错最好不要在其它地方引用该类
    """
    def __init__(self):
        self.a = 0


    def get_job_info(self, _id, name, trigger, func, args):
        return {
            "id": _id,
            "args": args,
            "name": name,
            "trigger": trigger,
            "func": self.get_func(func)
        }

    def add_job(self, _id, name, trigger, func, args, if_update=False):
        """
            增加一个定时任务
        """
        argss = {
            "args": args,
            "name": name,
            'trigger': trigger
        }
        job = scheduler.get_job(_id)  # type:Job
        print(f"更新定时任务:{_id}")
        if(if_update):
            if(job is not None):
                scheduler.remove_job(_id)
            scheduler.add_job(_id, self.get_func(func), **argss)
        else:
            if(job is None):
                scheduler.add_job(_id, self.get_func(func), **argss)
        tmp_scheduler = self.get_job_info(_id, name, trigger, func, args)

    def get_func(self, func):
        return f"scheduler.SchedulerMethod:{func.__name__}"


scheduler_factory = SchedulerFactory()

if (__name__ == "__main__"):
    scheduler_factory.add_job("1", 1, 1, scheduler_factory.get_job_info,1)

