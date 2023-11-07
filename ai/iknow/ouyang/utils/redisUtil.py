from dbconnection.redisConnection import redis_conn
import pickle

def get(key):
    data = redis_conn.get(key)
    return pickle.loads(data) if(data is not None) else None

def set(key, value):
    data = pickle.dumps(value)
    redis_conn.set(key,data)

def get_result(key, clasz):
    result = get(key)
    if(type(result) == clasz):
        return result
    elif(result is None):
        return None
    user = clasz()
    user.set_dict(result)
    return user

def set_result(key, data):
    set(key, data)

def delete(key):
    redis_conn.delete(key)