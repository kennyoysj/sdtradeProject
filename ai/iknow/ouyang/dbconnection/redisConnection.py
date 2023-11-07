import redis

from properties import *

redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=1)