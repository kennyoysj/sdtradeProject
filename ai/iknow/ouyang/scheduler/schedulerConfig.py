import datetime
import time
from apscheduler.executors.pool import ThreadPoolExecutor

from scheduler.SchedulerMethod import test, get_by_freq, calculate_hk_index, update_hk_index, update_cn_index
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
    jobs.append(scheduler_factory.get_job_info("test", "test", {
        "type": "cron",
        "hour": 22,
        "minute": 38,
        "second": 5
    }, test,None))
    jobs.append(scheduler_factory.get_job_info("get_by_freq", "get_by_freq", {
        "type": "interval",
        'seconds': 60
    }, get_by_freq, None))
    jobs.append(scheduler_factory.get_job_info("calculate_hk_index", "calculate_hk_index", {
        "type": "interval",
        'seconds': 60
    }, calculate_hk_index, None))
    jobs.append(scheduler_factory.get_job_info("update_hk_index", "update_hk_index", {
        "type": "cron",
        "hour": 16,
        "minute": 5,
        "second": 5
    }, update_hk_index, None))
    jobs.append(scheduler_factory.get_job_info("update_cn_index", "update_cn_index", {
        "type": "cron",
        "hour": 15,
        "minute": 5,
        "second": 5
    }, update_cn_index, None))
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
