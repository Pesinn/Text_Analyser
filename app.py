from os import listdir
from os.path import join
import file_process as fp

import nlp
import utils as ut
import sentiment
import gzip
import json
import pprint
import db_layer
import language
import multiprocessing as mp
import time

data_folder = "news_data"

# MULTI or empty
# MULTI: Multiple processed when creating annotating object.
# Empty for single process solution
process = "MULTI"

# "MANY" or empty
# MANY: Multiple inserts to mongodb.
# Empty: One article is inserted at a time.

# Keep in mind that upsert is not reliable
# when MANY is used. However, it is faster.
db_method = ""

# Only used for multiprocessing functionality.
# Indicates how many threads can be active at a time.
cpu_count = mp.cpu_count()

def beautify_print(t):
  json_str = pprint.pformat(t)
  print(json_str)

def process_files():
  l = listdir(data_folder)
  l.sort()
  for f in l:
    print(f)
    if can_be_processed(f):
      fp.set_processed(f)
      inner_folder = data_folder+"/"+f+"/per_day"
      files = listdir(inner_folder)
      files.sort()
      for i in files:
        date = i.replace(".gz", "")
        if file_can_be_processed(date):
          full_path = join(inner_folder, i)
          try:
            data = json.load(gzip.open(full_path))
            process_articles(data, f, date)
          except Exception as e:
            print(e)
            continue
          
          fp.set_processed_file(i)
      fp.delete_processed_file()

def process_articles(articles, news_source, date):
  if process == "MULTI":
    process_articles_multiprocess(articles, news_source, date)
  else:
    process_articles_singleprocess(articles, news_source, date)

def process_articles_singleprocess(articles, news_source, date):
  for a in articles:
    article_db = create_storage_article_obj(articles[a], a, news_source, date)

    if(article_db != {}):
      db_layer.save_object(article_db)

def process_articles_multiprocess(articles, news_source, date):
  pool = mp.Pool(cpu_count)
  limited_articles = []
  for a in articles:
    d = {
      "articles": articles[a],
      "id": a,
      "source": news_source,
      "date": date
    }

    limited_articles.append(d)
    if len(limited_articles) >= cpu_count:
      save_articles(pool.map(create_articles_obj, limited_articles))
      limited_articles = []
  pool.close()

def save_articles(data):
  if db_method == "MANY":
    db_layer.save_objects(data)
  else:
    for i in data:
      db_layer.save_object(i)

def create_articles_obj(article_arr):
  return create_storage_article_obj(
    article_arr["articles"],
    article_arr["id"],
    article_arr["source"],
    article_arr["date"])

# -----------------------------------------------------------
# Compare the date of input filename (yyyymmdd.gz) to the
# latest file that was processed in the processed.txt. To
# prevent same files to be processed twice.
# -----------------------------------------------------------
def file_can_be_processed(date):
  file_date = ut.convert_to_datetime(date)
  last_file_name = fp.get_latest_file()
  if(last_file_name == ""):
    return True
  else:
    last_file_date = ut.convert_to_datetime(last_file_name)
    if last_file_date < file_date:
      return True
  return False

def can_be_processed(name):
  if fp.is_finished(name) or name[-2:] == "fr" or name[-2:] == "de" or name[-2:] == "es" or name[-2:] == "it" or name[-2:] == "ru":
    return False
  return True

def create_storage_article_obj(article, id, news_source, date):
  lang = language.get_language(news_source)
  if(lang != "en"):
    return {}

  link = ""
  for i in article["link"]:
    link = i

  title_stripped = nlp.remove_irrelevant_text(article["title"])
  description_stripped = nlp.remove_irrelevant_text(article["description"])

  title_analysis = nlp.analyse_nlp(title_stripped, lang)
  description_analysis = nlp.analyse_nlp(description_stripped, lang)
  
  return {
    "_id": id,
    "article_language": lang,
    "publish_date": date[0:4]+"-"+date[4:6]+"-"+date[6:8],
    "source": news_source,
    "link": link,
    "annotations": {
      "entities": {
        "named": ut.combine_dictionaries(
            title_analysis["entities"],
            description_analysis["entities"]
        )
      },
      "sentiment_analysis":
        sentiment.combine_sentiment_scores(
          sentiment.sentiment_analysis(article["title"]),
          sentiment.sentiment_analysis(article["description"])),
    },
    "keywords": ut.remove_duplicate_words(title_analysis["all_tokens"] + " " + description_analysis["all_tokens"]),
    "title": {
      "text": title_stripped,
      "keywords": {
        "categorized": title_analysis["categorized"]
      }
    },
    "description" : {
      "text": description_stripped,
      "keywords": {
        "categorized": description_analysis["categorized"]
      }
    }
  }

def load_json():
  file = open('news_data.json',)
  data = json.load(file)
  file.close()
  return data

def sync_filters():
  sync_languages()
  sync_sources()
  
def sync_languages():
  l = db_layer.get_object("article_language")
  for i in l:
    try:
      db_layer.save_filter({"language": i})
    except Exception as e:
      print(e)
      continue

def sync_sources():
  s = db_layer.get_object("source")
  for i in s:
    try:
      db_layer.save_filter({"source": i})
    except Exception as e:
      print(e)
      continue

def startup():
  print("RC - ReCreate Database")
  print("PR - Process news articles")
  print("SY - Sync filters")
  print("I - Indexes")

  inp = input("What do you want to do?: ").upper()
  if inp == "RC":
    recreate_input()
  elif inp == "PR":
    process_files()
  elif inp == "I":
    indexes_input()
  elif inp == "SY":
    sync_filters()

def recreate_input():
  inp = input("Are you really sure? (write YES and press enter if you are): ")
  if inp == "YES":
    print("Recreating DB...")
    db_layer.recreate_db()

def indexes_input():
  print("C - Create")
  print("R - Remove")
  print("W - View")

  inp = input("").upper()
  if inp == "C":
    create_index_input()
  elif inp == "R":
    delete_index_input()
  elif inp == "W":
    db_layer.print_index_info()
  
def create_index_input():
  print("T - Create Text Index")
  print("W - Create Wildcard Index")
  print("R - Create Regular Index")
  inp = input("").upper()
  
  if inp == "T":
    print("Creating Text Index")
    db_layer.create_text_ind()
  elif inp == "W":
    print("Creating Wildcard Index")
    db_layer.create_wildcard_ind()
  elif inp == "R":
    db_layer.create_regular_ind()

def delete_index_input():
  print("A - Remove all indexes")
  print("T - Remove Text index")
  print("W - Remove Wildcard index")
  inp = input("").upper()

  if inp == "A":
    print("Removing All Indexes")
    db_layer.remove_all_indexes()
  elif inp == "T":
    db_layer.remove_text_ind()
  elif inp == "W":
    db_layer.remove_wildcard_ind()
  elif inp == "R":
    db_layer.remove_regular_ind()

startup()