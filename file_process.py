def set_processed(name):
  with open('processed.txt', 'a') as f:
    f.write(name + '\n')
    f.close()
    
def exist(name):
  data = get_processed()
  for i in data.split('\n'):
    if(name == i):
      return True
  return False

def get_processed():
  # Open a file: file
  with open('processed.txt',mode='r') as f:
    data = f.read()
    f.close()
    return data