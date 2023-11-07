import datetime
import time
from apscheduler.executors.pool import ThreadPoolExecutor

from scheduler.SchedulerMethod import test
from scheduler.SchedulerServer import scheduler_factory




def strftime(date_time):
    return date_time.strftime("%Y-%m-%d %H:%M:%S")

def init_scheduler():
    """
        初始化必须的task
        {
            'id': 'test',
            "name": "scheduler.SchedulerMethod:test",
            'func': "scheduler.SchedulerMethod:test",
            'trigger': "interval",
            'seconds': 60
        }
    """
    jobs = []
    jobs.append(scheduler_factory.get_job_info("static_times", "test", {
        "type": "cron",
        "hour": 9,
        "minute": 25
    }, test, ("param1",)))
    return jobs


class SchedulerConfig():
    SCHEDULER_EXECUTORS = {
        'default': ThreadPoolExecutor(20)  # 20个线程的线程池
    }
    SCHEDULER_JOB_DEFAULTS = {
        "job_defaults": {
            'coalesce': False,  # 是否合并执行
            'max_instances': 3  # 最大实例数
        }
    }
    DEFAULT_JOBS = init_scheduler()


if (__name__ == "__main__"):
    time.sleep(10)
    time.sleep(3)
