from os import listdir
from os.path import join
from datetime import date

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

def convert_to_datetime(_date):
    if(len(_date) <= 3 or len(_date) == 5 or len(_date) == 7 or len(_date) > 8):
        raise Exception(f"Input date cannot include {len(_date)} digits - it must contain 4,6 or 8")
    if(len(_date) == 4):
        return date(year=int(_date[0:4]), month=1, day=1)
    if(len(_date) == 6):
        return date(year=int(_date[0:4]), month=int(_date[4:6]), day=1)
    if(len(_date) == 8):
        return date(year=int(_date[0:4]), month=int(_date[4:6]), day=int(_date[6:8]))

def process_files():
  l = listdir(data_folder)
  l.sort()
  for f in l:
    inner_folder = data_folder+"/"+f+"/per_day"
    for i in listdir(inner_folder):
      full_path = join(inner_folder, i)
      try:
        d = json.load(gzip.open(full_path))
        for a in d:
          article_db = create_storage_article_obj(d[a], a, f, i)
          db_layer.save_object(article_db)
      except Exception as e:
        print(e)
        continue

def create_storage_article_obj(article, id, news_source, date):
  title_stripped = nlp.remove_unrelevant_text(article["title"])
  description_stripped = nlp.remove_unrelevant_text(article["description"])

  title_analysis = nlp.analyse_nlp(title_stripped, language.get_language(news_source))
  description_analysis = nlp.analyse_nlp(description_stripped, language.get_language(news_source))

  return {
    "article_id": id,
    "article_language": language.get_language(news_source),
    "publish_date": date[0:4]+"-"+date[4:6]+"-"+date[6:8],
    "source": news_source,
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
    "keywords": title_analysis["all_tokens"] + description_analysis["all_tokens"],
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

  inp = input("What do you want to do?: ")
  if(inp == "RC"):
    db_layer.recreate_db()
  elif(inp == "PR"):
    process_files()

startup()