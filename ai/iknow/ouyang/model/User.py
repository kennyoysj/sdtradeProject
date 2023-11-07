from dbconnection.mongoConnection import mongo_conn
from properties import user_col
from utils import AppUtil
from utils.AppUtil import generate_token


class User():
    '''
        {
            id,username,password,createTime,
            role(角色：web，ws),

        }
    '''
    def __init__(self):
        self.col = mongo_conn[user_col]

    def find_users_by_param(self, param):
        result = self.col.find(filter = param)
        return list(result)

    # 创建用户
    def add_user(self,user):
        id = generate_token()
        user["_id"] = id
        user["id"] = id
        user["createTime"] = AppUtil.get_now_timestamp()
        self.col.insert_one(user)

user_db = User()
if(__name__ == "__main__"):
    user = user_db.col.find_one({"username":"wsadmin"})
    print(user)
    # user_db.add_user({
    #     "username": "wsadmin",
    #     "password": md5("iknowadmin"),
    #     "createTime": AppUtil.get_now_timestamp(),
    #     "role": "ws",
    # })