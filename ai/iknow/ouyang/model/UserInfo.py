
class UserInfo(): # redis内保存的用户数据（登录）

    def __init__(self):
        self.username = None
        self.password = None
        self.sid = None

    def set_dict(self, data:dict):
        self.password = data.get("password")
        self.username = data.get("username")
        self.sid = data.get("sid")

    def get_dict(self):
        return {
            "password":self.password,
            "username": self.username,
            "sid": self.sid
        }




