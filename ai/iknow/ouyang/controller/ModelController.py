import datetime
import os

import pandas as pd
from flask import send_file

from properties import job_times, tushare_time_format, bms_result, hk_index_result, hk_average_result, cn_average_result
from utils.AppUtil import generate_result


class ModelController:


    def getResult(self):
        today = datetime.datetime.now().strftime(tushare_time_format)
        if(job_times.get("getBSM%s" % today,-1) < 0): return generate_result(200,"mission hasn't start")
        elif(job_times["getBSM%s" % today] < 100): return generate_result(200, "mission complete %s%s" % (str(job_times["getBSM"]),"%"))

        file_path = "result%s%s%s.csv" % (os.sep, "option_last_", today)
        return send_file(file_path)
    def BMSSigma(self,az:str):
        # keys = sorted(bms_result.keys())
        if(az is None or az.upper() == "CN"):
            result = bms_result
            for key in result.keys():
                result[key]["average_leverage"] = cn_average_result.get(key)
        elif(az.upper() == "HK"):
            result = hk_index_result
            for key in result.keys():
                result[key]["average_leverage"] = hk_average_result.get(key)
        return generate_result(200, result)



model_con = ModelController()
