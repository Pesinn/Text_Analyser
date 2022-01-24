def clean_text(text):
  text = remove_punctuations(text)
  return text

def remove_punctuations(text):
  punctuation='!?,.:;"\')(_-–’‘'
  ending = '\'’'
  new_text = ""
  latest = "--"
  c = 0
  num_to_del = 0
  for i in text:
    if num_to_del > 0:    
      latest = i
    else:
      if i not in punctuation:
        # Check for trailing 's
        if latest in ending:
          # Look for sometext's
          if i == "s":
            latest = i
            num_to_del = 1
          # If i == ll (like we'll)
          if i == 'l' and find(text, c+1) == 'l':
            latest = i
            num_to_del = 2
        else:
          new_text += i
          latest = i
      else:
        new_text += " "
        latest = i
    c += 1
    num_to_del -= 1
  return new_text

def find(list, index):
  obj = ""
  try:
    obj = list[index]
  except:
    obj = ""
  return obj