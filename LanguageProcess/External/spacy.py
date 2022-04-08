import spacy

nlp = spacy.load("en_core_web_lg")

def natural_language_process(text):
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
  stopword_filter = {"PUNCT", "ADV", "ADP", "SPACE"}
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
    text = (entity.text.strip()).lower()
    try:
      named_entity[text] = entity.label_
    except:
      named_entity[text] += entity.label_
  return named_entity

#natural_language_process("Bristol Myers Squibb Co, in New York, has reached $100 billion valuation. Not Bristol, the city.")