# redis
import datetime
import time
import os

mongo_uri = ""

redis_host = 'localhost'
redis_port = 6379

db = "modelDB"
user_col = "user"
config_col = "config"
check_result_col = "check_result"
scheduler_col = "scheduler"
tmp_scheduler_col = "tmp_scheduler"

ALLOWED_EXTENSIONS = ["csv"]

base_path = './data'

file_time_format = "%Y%m"
k_format = "%Y/%m/%d %H:%M:%S"
bao_time_format = "%Y-%m-%d"
tushare_time_format = "%Y%m%d"

file_suffix = '.csv'

def get_stock_file_name(code, time:datetime.datetime, freq):
    return code + "_" + time.strftime(file_time_format) + "_" + freq + file_suffix

encoding = "utf-8"

def getTimeStamp(t):
    if(isinstance(t, str)):
        t = datetime.datetime.strptime(t, "%Y%m%d%H%M%S%f")
    return int(time.mktime(t.timetuple()) * 1000)

# 阿里云参数
access_key_id = ""
access_key_secret = ""

project_base_path = os.path.dirname(os.path.abspath(__file__))