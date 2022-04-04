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

data_folder = "news_data"

def beautify_print(t):
  json_str = pprint.pformat(t)
  print(json_str)

def process_files():
  l = listdir(data_folder)
  l.sort()
  for f in l:
    print(f)
    if can_be_processed(f):
      inner_folder = data_folder+"/"+f+"/per_day"
      for i in listdir(inner_folder):
        full_path = join(inner_folder, i)
        try:
          d = json.load(gzip.open(full_path))
          for a in d:
            article_db = create_storage_article_obj(d[a], a, f, i)
            if(article_db != {}):
              db_layer.save_object(article_db)
        except Exception as e:
          print(e)
          continue
      fp.set_processed(f)

def can_be_processed(name):
  if fp.exist(name) or name[-2:] == "fr" or name[-2:] == "de" or name[-2:] == "es" or name[-2:] == "it" or name[-2:] == "ru":
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

def startup():
  print("RC - ReCreate Database")
  print("PR - Process news articles")
  print("I - Indexes")

  inp = input("What do you want to do?: ").upper()
  if inp == "RC":
    recreate_input()
  elif inp == "PR":
    process_files()
  elif inp == "I":
    indexes_input()

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