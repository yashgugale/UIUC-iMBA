import sys
import json
import common

def read_data(filename):

    try:            
        with open(filename, "r", encoding="utf-8") as f_data:
            data = f_data.readlines()
    except Exception as e:
        print("ERROR: Unable to read file. Exiting!")
        sys.exit(1)
    else:
        return data

# Save Emails, URLs, etc shared:
def save_metadata(data, data_type):

    data_list = []
    for item in data:
        comment = item[0]
        value = item[1][0]
        data_list.append({"Comment: ": comment, "Data: ": value})

    with open(common.CLASS_NAME + " - " + data_type + ".json", "w", encoding="utf-8") as f:
        f.write(json.dumps({data_type : data_list}, indent=4, default=str))

# Save the chat:
def save_chat(data, filename):

    data_list = []
    for line in data:
        sender = line[1]
        comment = line[0]
        data_list.append({sender: comment})

    with open(common.CLASS_NAME + " - " + filename + ".json", "w", encoding="utf-8") as f:
        f.write(json.dumps({"chats" : data_list}, indent=4, default=str))

