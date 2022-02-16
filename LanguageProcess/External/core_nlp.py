import stanza

nlp = stanza.Pipeline('en', processors="tokenize,ner")

def named_entities(text):
  doc = nlp(text)
  named_entity = {}
  
  """
  i holds the following attributes:
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