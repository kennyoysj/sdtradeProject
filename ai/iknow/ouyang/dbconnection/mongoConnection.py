import pymongo
from properties import *

mongo_conn = pymongo.MongoClient(host=mongo_uri)[db]
