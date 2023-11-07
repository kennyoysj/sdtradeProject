# -- coding:utf-8 --
import multiprocessing

from appConfig import app
# import backend
from apscheduler.jobstores.base import ConflictingIdError
from scheduler.Scheduler import scheduler
from scheduler.SchedulerServer import scheduler_factory
from scheduler.schedulerConfig import SchedulerConfig
import platform

if __name__ == '__main__':
    if platform.system() == "Windows":  # windows不允许多进程
        app.run('0.0.0.0', 5205, threaded=True, debug=False)
    else:
        app.config.from_object(SchedulerConfig())
        scheduler.init_app(app)
        scheduler.start()
        for each in SchedulerConfig.DEFAULT_JOBS:
            try:
                scheduler.add_job(**each)
            except ConflictingIdError:
                print("任务ID:", each.get("id"), "已经存在")
                pass
        scheduler_factory.bar_task()
        print(multiprocessing.cpu_count())
        app.run('0.0.0.0', 5205, debug=False)
