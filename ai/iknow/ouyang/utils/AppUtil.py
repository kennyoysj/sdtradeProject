import base64
import datetime
import hashlib
import smtplib
import uuid
from email.mime.text import MIMEText
from traceback import print_exc

import pytz
from flask import json
from flask import jsonify
from httpCode import http_code
from dbconnection.redisConnection import redis_conn
from model.UserInfo import UserInfo
from utils import redisUtil


def get_check_formData(need_list: list, option_list: list, request):
    """
    :param need_list:必须需要获取的param的名称列表
    :param option_list: 选择性获取的param的名称列表
    :param data: ImmutableMultiDict，从form表单中提取出来(此方法修改),改为对传入的jsonstr解析
    :return: 如果属性全部提取到的话就会返回Dict对象，data是结果，code为是否成功，1为成功，-1为未提取到所有对象，missing为缺少的属性列表
    """
    data = None
    if (request.method == 'POST'):
        b_data = request.get_data().decode()
        # data = eval(b_data.replace('\n', '').replace('\t', '')) if (b_data != '') else {}
        # print("b_data", b_data)
        data = json.loads(b_data) if (b_data != '') else {}
    elif (request.method == 'GET'):
        data = request.args
    # print('get_check_formData', data)
    return check_data(need_list, option_list, data)


def check_data(need_list: list, option_list: list, data):
    result_data = {}
    missing = []
    for i in range(len(need_list)):
        try:
            result = data[need_list[i]]
        except KeyError:
            result = None
        if (result == None):
            missing.append(need_list[i])
        else:
            result_data[need_list[i]] = result

    for i in range(len(option_list)):
        try:
            result = data[option_list[i]]
        except KeyError:
            result = None
        if (result != None and result != ''):
            result_data[option_list[i]] = result
    if (len(missing) > 0):
        return {'data': result_data, 'code': -1, 'missing': missing}
    return {'data': result_data, 'code': 1, 'missing': missing}


def get_check_form_data(need_list: list, option_list: list, request):
    '''
    此方法用于从请求中获取数据
    :param need_list:
    :param option_list:
    :param request:
    :return:
    '''
    form_data = request.form
    missing = []
    result_data = {}
    for each in need_list:
        result = form_data.get(each, None)
        if (result is None or result.strip() == ''):
            missing.append(each)
        else:
            result_data[each] = result.strip()
    for each in option_list:
        result = form_data.get(each, None)
        if (result is not None and result != ''):
            result_data[each] = result
    if (len(missing) > 0):
        return {'data': result_data, 'code': -1, 'missing': missing}
    return {'data': result_data, 'code': 1, 'missing': missing}


def generate_result(code=200, data=''):
    '''
    用于生成flask的标准回复
    :return: 标准回复
    '''
    return jsonify({
        'data': data,
        'message': http_code[str(code)]
    }), code


def generate_ws_result(code, data):
    '''
    用于生成flask的标准回复
    :return: 标准回复
    '''
    return {'data': data, 'message': http_code[str(code)], "code": code}


def generate_token(userName=None, password=None):
    if (userName is not None and password is not None):
        h = hashlib.md5()
        h.update("{0}:{1}".format(userName, password).encode())
        return h.hexdigest()
    return uuid.uuid4().hex


def check_ws_token(request):
    token = request.headers.get('token')
    user = redisUtil.get_result(token, UserInfo)  # type:UserInfo
    if (user is None):
        return False, user
    return True, user


def check_token(request):
    """
    这个方法用来检验token是否正确，没有或者错误就返回None， 有就返回role
    :return:
    """
    token = request.headers.get('token')
    if (token is None): return (False, None)
    result = redis_conn.get(token)
    result = eval(result) if result != None else None
    return (True, result) if result != None else (False, result)


def ws_token_verify(func):
    def wrapper(self, request, data, **kwargs):
        result, userInfo = check_ws_token(request)
        if (result):
            return func(self, data)
        return generate_ws_result(401, '')

    return wrapper


def parameter_verify_without_token(func):
    def wrapper(self, request, **kwargs):
        need_list = kwargs['need_list'] if 'need_list' in kwargs else []
        option_list = kwargs['option_list'] if 'option_list' in kwargs else []
        data = get_check_formData(need_list, option_list, request)
        if (data['code'] > 0):
            try:
                return func(self, data['data'])
            except Exception as e:
                print_exc()
                return generate_result(500, '')
        print('wrong parameters,missing:' + ','.join(data['missing']))
        return generate_result(400, 'wrong parameters,missing:' + ','.join(data['missing']))

    return wrapper


# from utils.CryptoUtil import decrypt
# def decrypt_parameter_verify_without_token(func):
#     def wrapper(self, request, **kwargs):
#         needs = ["data"]
#         need_list = kwargs['need_list'] if 'need_list' in kwargs else []
#         option_list = kwargs['option_list'] if 'option_list' in kwargs else []
#         data = get_check_formData(needs, [], request)["data"]
#         en = data["data"]
#         job = json.loads(decrypt(en))
#         data = check_data(need_list, option_list, job)
#         if (data['code'] > 0):
#             try:
#                 return func(self, data['data'])
#             except Exception as e:
#                 print_exc()
#                 return generate_result(500, '')
#         print('wrong parameters,missing:' + ','.join(data['missing']))
#         return generate_result(400, 'wrong parameters,missing:' + ','.join(data['missing']))


def parameter_verify(func):
    def wrapper(self, request, **kwargs):
        result, userInfo = check_token(request)
        if (result is False):
            return generate_result(401, '')
        role = userInfo['role']
        interface_need_role = kwargs['need_role'] if 'need_role' in kwargs else []
        if role not in interface_need_role:
            return generate_result(401, '')
        need_list = kwargs['need_list'] if 'need_list' in kwargs else []
        option_list = kwargs['option_list'] if 'option_list' in kwargs else []
        data = get_check_formData(need_list, option_list, request)
        if (data['code'] > 0):
            try:
                data['data']['userRole'] = role
                data['data']['userId'] = userInfo['id']
                return func(self, data['data'])
            except Exception as e:
                print_exc()
                return generate_result(500, '')
        print('wrong parameters,missing:' + ','.join(data['missing']))
        return generate_result(400, 'wrong parameters,missing:' + ','.join(data['missing']))

    return wrapper


def parameter_get(func):
    def wrapper(self, request, **kwargs):
        need_list = kwargs['need_list'] if 'need_list' in kwargs else []
        option_list = kwargs['option_list'] if 'option_list' in kwargs else []
        data = get_check_formData(need_list, option_list, request)
        if (data['code'] > 0):
            try:
                return func(self, data['data'])
            # except AutoReconnect as e:
            # 	print_exc()
            # 	return func(self, data['data'])
            except Exception as e:
                print_exc()
                return generate_result(500, '')
        print('wrong parameters,missing:' + ','.join(data['missing']))
        return generate_result(400, 'wrong parameters,missing:' + ','.join(data['missing']))

    return wrapper


def encode(string: str):
    # print(base64.standard_b64encode(string.encode('utf-8')))
    return base64.urlsafe_b64encode(string.encode('utf-8')).decode("utf-8")


def decode(string: str):
    missing_padding = 4 - len(string) % 4
    if missing_padding:
        string += '=' * missing_padding
    return base64.urlsafe_b64decode(string.encode("utf-8"))


# a = "eyJwYXNzcG9ydCI6IjU5Yjc5MzAzYjQ0MmM0MWRhMDNlMTgzMSIsInBhc3N3b3JkIjoiMTIzNDU2IiwidXNlck5hbWUiOiJ1c2VydGVzdDMifQ"
# print(decode(a))
# a = '{"passport":"59b79303b442c41da03e1831","password":"123456","userName":"usertest3"}'
# print(type(encode(a)))

def password_encrypt(password):
    '''
    用户密码加密
    :param password:
    :return:
    '''
    return hashlib.md5(password.encode('utf-8')).hexdigest()


def get_now_timestamp():
    '''
        获取当前时间戳的毫秒值
    '''
    # time.time() 获取到的时间戳是double
    return int(datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).timestamp() * 1000)


'''
    获取当前时间 以及sub天之前的数据，并且转换为tushare所需格式 eg 20200101
'''


def get_tushare_now_time(sub):
    now = datetime.datetime.now()
    now_sub = now - datetime.timedelta(days=sub)
    return str(now.replace(microsecond=0)), str(now_sub.replace(microsecond=0))


def format_datetime(time: str):
    date = time.split(" ")[0]
    date1 = time.split(" ")[1]
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    return year + "-" + month + "-" + day + " " + date1


# 发送邮件的方法
def send(to_list, sub, content, username, password, server_host):
    '''
    :param to_list: 收件人邮箱
    :param sub: 邮件标题
    :param content: 内容
    '''
    me = "manager" + "<" + username + ">"
    # _subtype 可以设为html,默认是plain
    msg = MIMEText(content, _subtype='html')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ';'.join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(server_host, 25)
        server.login(username, password)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    # print(get_tushare_now_time(5))
    print(format_datetime('20200812 15:00:00'))
