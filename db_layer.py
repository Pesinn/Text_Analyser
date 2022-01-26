import pymongo
import pprint
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

def recreate_db():
  drop_collection()
  remove_text_index()
  create_db()
  create_text_index()

def drop_collection():
  _mycol.drop()

def create_db():
  name = "news_data_TEST"
  db = _myclient[name]
  list_of_db = _myclient.list_database_names()
  
  print("All collections:")
  for i in list_of_db:
    print("- ", i)

def remove_text_index():
  name = "$**_text"
  _mycol.drop_index(name)

  print(f"List of indexes left after removing {name}")
  pprint.pprint(_mycol.index_information())
  
def create_text_index():
  response = _mycol.create_index([("$**", pymongo.TEXT)],
                        language_override="article_language")
  print(response)
  print(f"List of indexes after adding creating new")
  pprint.pprint(_mycol.index_information())