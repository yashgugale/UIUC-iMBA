from importlib.util import spec_from_file_location
from corpus import ZoomCorpus 
from pre_processing import PreProcessing
from collections import Counter
from nltk.corpus import stopwords
# Use the following to download the packages to appropirate location:
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.tokenize import word_tokenize

COURSE_NAME = "BADM 508"
CORPUS_PATH = r"D:/40-UIUC iMBA/MBA Program Materials/UIUC-IMBA Projects/Zoom meeting chat analysis/Courses/Corpus/" + COURSE_NAME

def read_corpus():
    zoom_corpus = ZoomCorpus(COURSE_NAME, CORPUS_PATH)
    docs = zoom_corpus.docs(zoom_corpus.fileids()[1:3])
    sizes = zoom_corpus.sizes(zoom_corpus.fileids())
    # print(list(docs))
    # print(list(sizes))

 
    corpus_processing = PreProcessing(zoom_corpus)
    # print(corpus_processing)
    # print(dir(corpus_processing))

    tokens = corpus_processing.tokenize()
    tokens_lowercase = corpus_processing.make_lower(tokens)
    tokens_without_sw = corpus_processing.remove_stopwords(tokens_lowercase)
    tokens_without_spec_chars = corpus_processing.remove_spec_chars(tokens_without_sw, log=True)
    

    # count = Counter(categorized_corpus.words())
    # count = count.most_common()
    # print(count)
    # print(dir(count))
    # print("Elements: ", count.elements())
    # print("Items: ", count.items())
    # print("Keys: ", count.keys())
    # print("Values: ", count.values())

    # print(count)
    # print(*count.most_common(), sep="\n")

 
    # # 2: TODO: Spell checker and corrector here

 
    # # 5: Create counter:
    # count = Counter(tokens_without_sw)
    # count = count.most_common()
    # print(*count, sep="\n")
    # print("5: Len count: ", len(count))




read_corpus()