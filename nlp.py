from numpy import split
import LanguageProcess.External.spacy as sp
import LanguageProcess.External.nlp_nltk as nltk
import LanguageProcess.NLP.en as english

import utils as ut
from spacy.language import Language
from spacy_langdetect import LanguageDetector

def get_lang_detector(nlp, name):
    return LanguageDetector()

#def add_language_detector():
#  Language.factory("language_detector", func=get_lang_detector)
#  nlp.add_pipe('language_detector', last=True)

# Sentences that should be ignored
ignore_array = ["Breaking UK News & World News Headlines",
                "Daily Star"]

def analyse_nlp(text, lang):
  text = clean_text(text, lang)
  # Get data from Spacy
  nlp_data = sp.natural_language_process(text)

  # Get named entities from nltk
  named_ent = nltk.named_entities_nltk(text)
  
  nlp_data["entities"] = combine_named_entities(
    nlp_data["entities"],
    named_ent
  )

  return nlp_data

# N1 entities should be the leading data
# if N2 does not exist in N1, then it
# should be added to N1
def combine_named_entities(n1, n2):  
  entities = n1
  found = False
  
  if(entities == {}):
    return n2
  elif(n2 == {}):
    return n1
  
  for i in n2:
    for a in n1:
      if(i == a):
        found = True

    if (found == False):
      entities[i] = n2[i]
    found = False

  return entities

def detect_language(doc):
  lang = doc._.language["language"]
  # MongoDB doesn't handle 'id' as langauge
  if lang == "id":
    return "indonesian"
  return lang

def clean_text(text, lang):
  if(lang == "en"):
    text = english.clean_text(text)
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

# Split array by specific character
def split_array(arr, split_by):
  result_arr = []
  for i in arr:
    second_split = i.split(split_by)
    for s in second_split:
      result_arr.append(s.strip())
  return result_arr