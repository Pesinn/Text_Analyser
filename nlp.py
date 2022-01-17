from numpy import split
import spacy
import pprint

from spacy.language import Language
from spacy_langdetect import LanguageDetector

nlp = spacy.load("en_core_web_sm")

def get_lang_detector(nlp, name):
    return LanguageDetector()

#def add_language_detector():
#  Language.factory("language_detector", func=get_lang_detector)
#  nlp.add_pipe('language_detector', last=True)

# Sentences that should be ignored
ignore_array = ["Breaking UK News & World News Headlines",
                "Daily Star"]

def analyse_nlp(text):
  text = clean_text(text)
  print(text)
  doc = nlp(text)
  tokens = get_tokens(doc)

  nlp_data = {
    "categorized": tokens[0],
    "entities": get_named_entities(doc),
    "all_tokens": tokens[1].strip()
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
def get_tokens(doc):
  all_stopwords = nlp.Defaults.stop_words
  stopword_filter = {"PUNCT", "ADV", "ADP"}
  categorized = {}
  all_tokens = ""
  for token in doc:
    if token.text not in all_stopwords and token.pos_ not in stopword_filter:
      obj = {token.text: {"l": token.lemma_.lower()}}
      try:
        # Objects should be unique
        if(obj not in categorized[token.pos_]):
          categorized[token.pos_].append(obj)
      except:
        categorized[token.pos_] = [obj]    
      all_tokens += token.lemma_.lower()
      all_tokens += " "
  return categorized, all_tokens


"""
Returns data such as
{
  'Al Jazeera': 'ORG',
  'Asia Pacific': 'LOC',
  'China': 'GPE',
  'Hong Kong': 'GPE'
  }
}
"""
def get_named_entities(doc):
  named_entity = {}
  for entity in doc.ents:
    text = entity.text.lower()
    try:
      named_entity[text] = entity.label_
    except:
      named_entity[text] += entity.label_
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

def clean_text(text):
  text = remove_punctuations(text)
  text = remove_ending(text)
  return text

def remove_punctuations(text):
  punctuation='!?,.:;"\')(_-'
  new_text = ""
  for i in text:
    if(i not in punctuation):
      new_text += i
  return new_text


# Remove ending such as '’s'
# Example: "Tesla’s latest Roadster model"
def remove_ending(text):
  i = 0
  found = False
  new_text = ""
  while i < len(text):
    if(text[i] == '’'):
      found = True
    else:
      if(found == True and text[i] == "s"):
        found = False
      else:
        new_text += text[i]
    i += 1

  return text

# Getting rid of a text like:
# "... | Daily News"
# or
# "... - Daily News"
def remove_unrelevant_text(text):
  if not text:
    return ""

  split_arr = text.split("|")
  s = split_array(split_arr, " - ")

  # If text chunk contains less than 6 words
  # we consider it as an unrelevant text.
  # The reason is that an article will never
  # only have 5 words in the title nor the description

  article_text = ""
  for i in s:
    if(len(i.split()) > 5):
      if(i not in ignore_array):
        if(len(article_text) == 0):
          article_text = i
        else:
          article_text += f" {i}"
  return article_text.strip()

def split_array(arr, split_by):
  result_arr = []
  for i in arr:
    second_split = i.split(split_by)
    for s in second_split:
      result_arr.append(s.strip())
  return result_arr