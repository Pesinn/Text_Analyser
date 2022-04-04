from datetime import date

def combine_dictionaries(dict1, dict2):
  merged = dict()
  merged.update(dict1)
  merged.update(dict2)
  return merged

def remove_duplicate_words(str):
  words = str.split()
  return " ".join(sorted(set(words), key=words.index))


# Convert string to date object
# Input pattern: yyyymmdd
def convert_to_datetime(_date):
  if _date.isdecimal():
    if(len(_date) <= 3 or len(_date) == 5 or len(_date) == 7 or len(_date) > 8):
      raise Exception(f"Input date cannot include {len(_date)} digits - it must contain 4,6 or 8")
    if(len(_date) == 4):
      return date(year=int(_date[0:4]), month=1, day=1)
    if(len(_date) == 6):
      return date(year=int(_date[0:4]), month=int(_date[4:6]), day=1)
    if(len(_date) == 8):
      return date(year=int(_date[0:4]), month=int(_date[4:6]), day=int(_date[6:8]))
  else:
    raise Exception("Input date can only contan digits (like: 20200101)")