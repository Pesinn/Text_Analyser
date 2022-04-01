from heapq import merge


def combine_dictionaries(dict1, dict2):
  merged = dict()
  merged.update(dict1)
  merged.update(dict2)
  print(merged)
  return merged

def remove_duplicate_words(str):
  words = str.split()
  return " ".join(sorted(set(words), key=words.index))