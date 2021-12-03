from os import listdir
from os.path import join
from datetime import date

import nlp
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

def combine_dictionaries(dict1, dict2):
  merged = dict()
  merged.update(dict1)
  merged.update(dict2)
  return merged

def process_files():
  for f in listdir(data_folder):
    inner_folder = data_folder+"/"+f+"/per_day"
    for i in listdir(inner_folder):
      full_path = join(inner_folder, i)
      try:
        d = json.load(gzip.open(full_path))
        for a in d:
          title_analysis = nlp.analyse_nlp(d[a]["title"], language.get_language(f))
          description_analysis = nlp.analyse_nlp(d[a]["description"], language.get_language(f))
          obj = {
            "article_id": a,
            "article_language": language.get_language(f),
            "publish_date": i[0:4]+"-"+i[4:6]+"-"+i[6:8],
            "source": f,
            "annotations": {
              "entities": {
                "named": combine_dictionaries(
                    title_analysis["entities"],
                    description_analysis["entities"]
                )
              },
              "sentiment_analysis":
                sentiment.combine_sentiment_scores(
                  sentiment.sentiment_analysis(d[a]["title"]),
                  sentiment.sentiment_analysis(d[a]["description"]))
            },
            "title": {
              "text": d[a]["title"],
              "keywords": {
                "categorized": title_analysis["categorized"]
              }
            },
            "description" : {
              "text": d[a]["description"],
              "keywords": {
                "categorized": description_analysis["categorized"]
              }
            }
          }
          db_layer.save_object(obj)          
      except Exception as e:
        print(e)
        continue

def load_json():
  file = open('news_data.json',)
  data = json.load(file)
  file.close()
  return data

process_files()

#print(language.get_language("9news.com.au"))

#print(nlp.remove_unrelevant_text("Hashd deputy Abu Mahdi al-Muhandis: Iran’s man in Baghdad | Iraq | Al Jazeera"))