import json
from dotenv import dotenv_values

config = dotenv_values()

def write_json(new_data, filename=config["UserData"]):
  with open(filename,'r+') as file:
    print(new_data)
    file_data = json.load(file)
    file_data["users"].append(new_data)
    file.seek(0)
    json.dump(file_data, file, indent = 4)


def delete_json(remove_data, filename=config["UserData"]):
  with open(filename, 'r+') as file:
    file_data = json.load(file)
    user_list = file_data["users"]
    for i in range(0, len(user_list)-1):
      if user_list[i]["user_name"] == remove_data["user_name"]:
        user_list.pop(i)
    file.seek(0)

  with open(filename, 'w', encoding='utf-8') as file:
    file.write(json.dumps(file_data, indent=2))

def read_json(filename = config["UserData"]):
  with open(filename, 'r') as file:
    file_data = json.load(file)
  return file_data["users"]