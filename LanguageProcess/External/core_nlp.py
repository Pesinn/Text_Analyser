import stanza
from stanza.server import CoreNLPClient

nlp = stanza.Pipeline('en', processors="tokenize,ner")
tool = "STANZA"

def named_entities(text):
  if tool == "STANZA":
    return named_entities_stanza(text)
  else:
    return named_entities_corenlp(text)

def named_entities_corenlp(text):
  entities = []
    
  with CoreNLPClient(properties='english', annotators='ner', output_format='json') as client:
    d = client.annotate(text, properties="en")
    for i in d["sentences"]:
      for t in i["tokens"]:
        if t["ner"] != "O":
          e = {
            "text": t["word"],
            "type": t["ner"]
          }
          entities.append(e)
  
  named_entity = {}
  
  for item in entities:
    try:
      named_entity[item["text"].lower()] = item["type"]
    except:
      named_entity[item["text"].lower()] += item["type"]

  return named_entity


def named_entities_stanza(text):    
  doc = nlp(text)
  named_entity = {}

  """
  item holds the following attributes:
  - text
  - type
  - start_char
  - end_char
  """
  for item in doc.entities:
    try:
      named_entity[item.text.lower()] = item.type
    except:
      named_entity[item.text.lower()] += item.type

  return named_entity