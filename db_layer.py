import pymongo
from pymongo import (common, helpers, message)

_myclient = pymongo.MongoClient('localhost', 27017)
_dbList = _myclient.list_database_names()

_mydb = _myclient["news_data_TEST"]
_mycol = _mydb["news_data"]

print("Databases: ", _dbList)

def save_object(object):
  k = {"article_id": object["article_id"]}
  x = _mycol.update(k, object, upsert=True)
  #print(x)

def save_objects(objects):
  x = _mycol.insert_many(objects)
  print(x.inserted_ids)