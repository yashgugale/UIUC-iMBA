from data_io import read_data, save_metadata, save_chat
from data_manipulation import extract_comments, sort_comments, filter_by_word_count
from data_plot import plot_word_count
from metadata import find_useful_metadata
from chat_analysis import extract_conversation
import sys
import common
import os

def main():

    common.CLASS_NAME = "BADM_572/BADM_572"
    if not os.path.exists("BADM_572"):
        os.makedirs("BADM_572")

    # Read Data:
    chat_data = read_data("BADM-572-LiveSession-1-01132021-6pm.txt")

    # Extract sentences:
    chat = extract_comments(chat_data)
    # print(*chat, sep="\n")
    # Sort comments by word frequency:
    sorted_chat = sort_comments(chat)
    plot_word_count(sorted_chat, "Frequency of comments with word count")
    # print(*sorted_chat, sep="\n")

    # Filter comments by word count:
    count = 13
    filtered_chat = filter_by_word_count(chat, count)
    # print(*filtered_chat, sep="\n")
    plot_word_count(sort_comments(filtered_chat), "Frequency of comments with word count greater than " + str(count-1))
    save_chat(filtered_chat, "Filtered chat with word count greater than " + str(count-1))

    # Find email, URLs, etc in the chat:
    email_list, url_list = find_useful_metadata(chat_data)
    save_metadata(email_list, "emails")
    save_metadata(url_list, "urls")

    # Create conversation:
    extract_conversation(chat)


if __name__ == "__main__":
    main()