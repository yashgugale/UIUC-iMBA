import re

def extract_comments(data):

    chat = []
    sender = ""
    for i in range(len(data)):

        # Detect for timestamp. If present, extract message Sender:
        if re.match('\d{2}:\d{2}:\d{2}', data[i]):
            sender = re.search('From (.*) to', data[i]).group(1).strip()
        
        # Line is their comment:
        else:
            comment = data[i].strip()
            word_count = len(comment.split())
            chat.append([comment, sender, word_count])
        
    return chat

# Sort the chat by word count:
def sort_comments(data):

    sorted_chat = sorted(data, key=lambda x:x[2])
    return sorted_chat

def filter_by_word_count(data, count):

    filtered_data = [line for line in data if line[2] >= count]
    return filtered_data


