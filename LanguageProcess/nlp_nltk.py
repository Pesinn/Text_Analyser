from cgitb import text
from os import remove
import nltk
from nltk.tree import Tree
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

def _speech_tag(word_list):
  return nltk.pos_tag(word_list)

def _named_entities_chunk(tagged_list):
  return nltk.ne_chunk(tagged_list)

def _stopwords(lang):
  return stopwords.words(lang)

def remove_stopwords(text_list):
  result_list = []
  swords = _stopwords("english")
  for i in text_list:
    if i.lower() not in swords:
      result_list.append(i)
  return result_list

def clean_text(text_list):
  text_list = remove_stopwords(text_list)
  return text_list

# Make sure to capture full names into
# single entitiy
def text_to_list(text):
  text_list = []
  prev = ""
  for i in text.split():
    if(i[0].isupper() == True):
      if(i.isupper()):
        if(len(prev) > 0):
          text_list.append(prev)
        text_list.append(i)
        prev = ""
      elif(prev == ""):
        prev += i
      else:
        prev += " "
        prev += i
    else:
      if(prev == ""):
        text_list.append(i)
        prev = ""
      else:
        text_list.append(prev)
        text_list.append(i)
        prev = ""
  return text_list

def named_entities_nltk(text):
  text_list = text_to_list(text)
#  text_list = word_tokenize(text)
  cleaned = clean_text(text_list)

  tagged = _speech_tag(cleaned)
  chunk = _named_entities_chunk(tagged)
  
  items = nltk.chunk.tree2conlltags(chunk)
  
  named_entity = {}
  for item in items:
    try:
      named_entity[item[0].lower()] = item[1]
    except:
      named_entity[item[0].lower()] += item[1]

  return named_entity