import spacy
import pprint

from spacy.language import Language
from spacy_langdetect import LanguageDetector

nlp = spacy.load("en_core_web_sm")

def get_lang_detector(nlp, name):
    return LanguageDetector()

def add_language_detector():
  Language.factory("language_detector", func=get_lang_detector)
  nlp.add_pipe('language_detector', last=True)

add_language_detector()

def analyse_nlp(text):
  """
  text = ("When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously wherever he was angry. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week.")
  """
  doc = nlp(text)

  nlp_data = {
    "language": detect_language(doc),
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
      named_entity[entity.text] = entity.label_
    except:
      named_entity[entity.text] += entity.label_
  return named_entity

def detect_language(doc):
  lang = doc._.language["language"]
  # MongoDB doesn't handle 'id' as langauge
  if lang == "id":
    return "indonesian"
  return lang

def testing(text):
  doc = nlp(text)
  print(detect_language(doc))