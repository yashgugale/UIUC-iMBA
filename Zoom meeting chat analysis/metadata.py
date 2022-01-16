import re

def find_useful_metadata(data):

    email_list = []
    url_list = []
    for line in data:
        line = line.strip()
        # Email:
        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', line)
        if(emails):
            email_list.extend([[line, emails]])
            # print(emails)

        # URLs:
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        urls_match = re.findall(regex, line)
        urls = [x[0] for x in urls_match]
        if urls:
            url_list.extend([[line, urls]])
            # print(urls)
    
    # print("\nEmail list: ", email_list)
    # print("Url list: ", url_list)
    return email_list, url_list    
