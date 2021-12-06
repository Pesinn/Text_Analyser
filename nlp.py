from numpy import split
import spacy
import pprint

from spacy.language import Language
from spacy_langdetect import LanguageDetector

nlp = spacy.load("en_core_web_sm")

def get_lang_detector(nlp, name):
    return LanguageDetector()



# It sucks
#def add_language_detector():
#  Language.factory("language_detector", func=get_lang_detector)
#  nlp.add_pipe('language_detector', last=True)

# Sentences that should be ignored
ignore_array = ["Breaking UK News & World News Headlines"]

def analyse_nlp(text, lang):
  doc = nlp(remove_unrelevant_text(text))

  nlp_data = {
    "categorized": get_categorized(doc),
    "entities": get_named_entities(doc)
  }

  return nlp_data

"""
Returns data such as:
{
  'ADP':  [
    {'amid': {'l': 'amid'}}
  ],
  'NOUN': [
    {'liaison': {'l': 'liaison'}},
    {'office': {'l': 'office'}},
    {'head': {'l': 'head'}},
    {'protests': {'l': 'protest'}}
  ]
}
"""
def get_categorized(doc):
  all_stopwords = nlp.Defaults.stop_words
  stopword_filter = {"PUNCT", "ADV"}
  categorized = {}
  for token in doc:
    if token.text not in all_stopwords and token.pos_ not in stopword_filter:
      obj = {token.text: {"l": token.lemma_}}
      try:
        # Objects should be unique
        if(obj not in categorized[token.pos_]):
          categorized[token.pos_].append(obj)
      except:
        categorized[token.pos_] = [obj]
  return categorized


"""
Returns data such as
{
  'Al Jazeera': 'ORG',
  'Asia Pacific': 'LOC',
  'China': 'GPE',
  'Hong Kong': 'GPE'}
}
"""
def get_named_entities(doc):
  named_entity = {}
  for entity in doc.ents:
    try:
      named_entity[entity.text.lower()] = entity.label_
    except:
      named_entity[entity.text.lower()] += entity.label_
  return named_entity

def convert_dict_to_list(dict):
  l = []
  for i in dict:
    l.append({
      "entity": i,
      "count": dict[i]["count"],
      "type": dict[i]["type"]
    })
  return l
  
def detect_language(doc):
  lang = doc._.language["language"]
  # MongoDB doesn't handle 'id' as langauge
  if lang == "id":
    return "indonesian"
  return lang

def testing(text):
  doc = nlp(text)
  print(doc)
  
def remove_unrelevant_text(text):
  if not text:
    return ""
  
  split_arr = text.split("|")

  # If text chunk contains less than 6 words
  # we consider it as an unrelevant text.
  # The reason is that an article will never
  # only have 5 words in the title nor the description
  article_text = ""
  for i in split_arr:
    if(len(i.split()) > 5):
      if(i not in ignore_array):
        if(len(article_text) == 0):
          article_text = i
        else:
          article_text += f" {i}"
  return article_text