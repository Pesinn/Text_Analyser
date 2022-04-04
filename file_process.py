file_name = "processed.txt"

def overwrite_file(data):
  if data != "":    
    store_str = ""
    for i in data:
      i = i.strip()
      if i != "" and i != '\n':
        store_str += i + '\n'
    
    with open(file_name, 'w') as f:
      f.write(store_str)
      f.close()

def set_processed(name):
  # Check if last element is a file
  # if so, then do nothing
  last = get_processed_lines()[-1:]
  if last != []:
    last[0] = last[0].strip()
    if last[0][:1] == "-":
      return 

  with open(file_name, 'a') as f:
    f.write(name + '\n')
    f.close()

def set_processed_file(file):
  last = get_processed_lines()[-1:]
  if last != []:
    last[0] = last[0].strip()
    new_file_data = []

    # If true we know that last element in
    # the file contains a file name ("- filename")    
    if last[0][:1] == "-":
      new_file_data = get_processed_lines()[:-1]
    else:
      new_file_data = get_processed_lines()
            
    new_file_data.append("- " + file.replace(".gz", ""))
    overwrite_file(new_file_data)
  else:
    raise Exception("The first element in the file should not be a filename")

def delete_processed_file():
  last = get_processed_lines()[-1:]
  if last != []:
    last[0] = last[0].strip()
    # If true we know that last element in
    # the file contains a file name ("- filename")    
    if last[0][:1] == "-":
      overwrite_file(get_processed_lines()[:-1])

def is_finished(name):
  data = get_processed_lines()[:-2]
  for i in data:
    if(name == i.strip()):
      return True
  return False

def get_processed():
  with open(file_name,mode='r') as f:
    data = f.read()
    f.close()
    return data

def get_latest_file():
  last = get_processed_lines()[-1:]
  if last != []:
    last[0] = last[0].strip()

    # If true we know that last element in
    # the file contains a file name ("- filename")    
    if last[0][:1] == "-":
      return last[0].replace("- ", "")
  return ""

def get_processed_lines():
  with open(file_name,mode='r') as f:
    data = f.readlines()
    f.close()
    return data
