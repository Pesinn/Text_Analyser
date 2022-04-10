from langcodes import DEFAULT_LANGUAGE
import pymongo
import pprint
from pymongo import (common, helpers, message)

_myclient = pymongo.MongoClient('localhost', 27017)
_dbList = _myclient.list_database_names()

db_name = "news_data_TEST"
_mydb = _myclient[db_name]
_mycol = _mydb["news_data"]

_index_names = {
  "TEXT": {"name": "text_index", "fields": "keywords"},
  "WILDCARD": {"name": "wildcard_index", "fields": "$**"},
  "REGULAR": {"name": "regular_index", "fields": "keywords"}
}

print("Databases: ", _dbList)

def save_object(object):
  k = {"_id": object["_id"]}
  x = _mycol.update(k, object, upsert=True)

def save_objects(objects):
  x = _mycol.insert_many(objects)

def recreate_db():
  drop_collection()
  create_db()
  
def drop_collection():
  _mycol.drop()

def create_db():
  _myclient[db_name]
  list_of_db = _myclient.list_database_names()
  
  print("All collections:")
  for i in list_of_db:
    print("- ", i)

def recreate_indexes(type):
  remove_index(type)
  create_index(type)

def remove_all_indexes():
  for i in _index_names:
    remove_index(i)

def remove_wildcard_ind():
  remove_index("WILDCARD")

def remove_text_ind():
  remove_index("TEXT")
  
def remove_regular_ind():
  remove_index("REGULAR")
  
def create_wildcard_ind():
  create_index("WILDCARD")
  
def create_text_ind():
  create_index("TEXT")
  
def create_regular_ind():
  create_index("REGULAR")

def create_index(type):
  try:
    response = ""
    if type == "TEXT" or type == "WILDCARD":
      response = create_text_index(type)
    else:
      response = create_regular_index_by_type(type)
    print(response)
    print_index_info()
  except Exception as error:
    print(f"exception when creating an index with type {type}", error)
    
def create_text_index(type):
  return _mycol.create_index(
    [(_index_names[type]["fields"], pymongo.TEXT)],
    language_override="article_language",
    name=_index_names[type]["name"])

def create_regular_index_by_type(type):
  return _mycol.create_index(
    [(_index_names[type]["fields"], pymongo.DESCENDING)],
    language_override = "article_language",
    name=_index_names[type]["name"])

def remove_index(type):
  try:
    print(type)
    index_name = _index_names[type]["name"]
    print(f"Removing index {index_name}")
    _mycol.drop_index(index_name)
    print_index_info()
  except Exception as error:
    print(f"exception when removing an index with type {type}", error)

def print_index_info():
  print(f"List of indexes")
  pprint.pprint(_mycol.index_information())
