from numpy import split
import LanguageProcess.spacy as sp
import LanguageProcess.nlp_nltk as nltk
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

def analyse_nlp(text):
  text = clean_text(text)

  # Get data from Spacy
  nlp_data = sp.natural_language_process(text)

  # Get named entities from nltk
  named_ent = nltk.named_entities_nltk(text)

  named_ent["entities"] = ut.combine_dictionaries(
    nlp_data["entities"],
    named_ent
  )
  return nlp_data


def detect_language(doc):
  lang = doc._.language["language"]
  # MongoDB doesn't handle 'id' as langauge
  if lang == "id":
    return "indonesian"
  return lang

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

  return new_text

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