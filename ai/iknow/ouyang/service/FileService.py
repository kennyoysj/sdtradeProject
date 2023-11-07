import csv

from utils.AppUtil import *


class FileService():

    def upload(self, data):
        path = data['path']
        model = data['model']
        stock = data['stock']
        d = {}
        with open(path) as f:
            render = csv.reader(f)  # reader(迭代器对象)--> 迭代器对象
            # 取表头
            header_row = next(render)
            # print(header)
            for row in render:
                date = datetime.datetime.strptime(row[1],'%Y-%m-%d %H:%M:%S')
                predict = row[3]
                d[date] = {'date':date,'predict':predict}
        list1 = list(d.keys())
        list1.sort()
        last_d = d[list1[-1]]
        # mycol = mongo_conn["sites"]
        # res = list(mycol.find({'model_name': model, 'stock_name':stock, 'time':last_d['date'],'version':'update'}))
        # if (len(res) > 0):
        #     id = res[0]['id']
        #     mycol.update_one({'id': id}, {'$set': {'predict_close': last_d['predict']}})
        # else:
        #     d = {'id': generate_token(), 'model_name': model, 'stock_name': stock, 'time': last_d['date'],
        #          'predict_close': last_d['predict'], 'version': 'update'}
        #     mycol.insert_one(d)
        return generate_result(200,"")

file_service = FileService()