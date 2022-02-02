def clean_text(text):
  text = remove_punctuations(text)
  return text

def remove_punctuations(text):
  punctuation='!?,.:;"\')(_-–’‘'
  new_text = ""
  for i in text:
    if i not in punctuation:
      new_text += i
  return new_text