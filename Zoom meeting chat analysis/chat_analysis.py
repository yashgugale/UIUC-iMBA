import re
import json
import common

def search_response(question_line, next_few_lines):

    responses = []
    # Get the first name:
    sender_name = question_line[1]
    first_name = sender_name.split()[0].lower()
    responses.append("Q: " + question_line[0])
    
    for line in next_few_lines:
        # print(line[0])
        name_response = re.findall(r'@\w+', line[0])
        if(name_response):
            response_to = name_response[0].strip('@').lower()
            # print(response_to)
            if(first_name == response_to):
                ans = re.sub(r"[^a-zA-Z0-9\s*]","", line[0].strip(name_response[0]))
                responses.append("A: " + ans.strip())

    print(responses)
    # return {"chat: ", json.dumps(responses)}
    # return json.dumps(responses, indent=4)
    return responses


def extract_conversation(data):

    conversations = []

    question_re = re.compile(r"\w+\?\s*")

    for i in range(len(data)):
        match = question_re.findall(data[i][0])
        if match:
            # print(data[i])
            response = search_response(data[i], data[i:i+30])
            conversations.append(response)
            # break

    with open(common.CLASS_NAME + " - converations.json", "w", encoding="utf-8") as f:
        # f.write(conversations)
        f.write(json.dumps({"chats" : conversations}, indent=4, default=str))
