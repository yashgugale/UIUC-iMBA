import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import common

def plot_word_count(data, title):

    word_count_list = []
    for line in data:
        word_count = line[2]
        word_count_list.append(word_count)
    count = Counter(word_count_list)
    # labels, values = zip(*Counter(['A','B','A','C','A','A']).items())
    labels, values = zip(*Counter(word_count_list).items())

    indexes = np.arange(len(labels))
    width = 0.8

    fig = plt.figure(figsize=(20,10))
 
    plt.bar(indexes, values, width)
    plt.xlabel("Number of words in comment")
    plt.ylabel("Frequency of Comments")
    plt.title(title)
    plt.xticks(indexes, labels)
    # plt.show()
    plt.savefig(common.CLASS_NAME + " - " + title + '.png')



