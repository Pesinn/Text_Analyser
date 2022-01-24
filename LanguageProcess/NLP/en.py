def clean_text(text):
  text = remove_punctuations(text)
  return text

def remove_punctuations(text):
  punctuation='!?,.:;"\')(_-–'
  ending = '\''
  new_text = ""
  latest = ""
  for i in text:
    if i not in punctuation:
      if latest in ending and latest is not "":
        latest = i
      else:
        new_text += i
        latest = i
    else:
      # Check for trailing 's
      if i in ending:
        new_text += " "
        latest = i
  return new_text