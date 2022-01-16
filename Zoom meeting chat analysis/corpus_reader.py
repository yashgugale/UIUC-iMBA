from importlib.util import spec_from_file_location
from corpus import Corpus 
from collections import Counter
from nltk.corpus import stopwords
# Use the following to download the packages to appropirate location:
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.tokenize import word_tokenize

COURSE_NAME = "BADM 508"
CORPUS_PATH = r"D:/40-UIUC iMBA/MBA Program Materials/Zoom Meeting Chat Analysis/Courses/Corpus/" + COURSE_NAME

def read_corpus():
    corpus = Corpus(COURSE_NAME, CORPUS_PATH)
    categorized_corpus = corpus.categorized_plain_text_corpus_reader()

    # print(categorized_corpus.categories())
    # print(categorized_corpus.fileids())
    # print(dir(categorized_corpus))
    # print(categorized_corpus.citation())
    # print(categorized_corpus.encoding())
    # print(categorized_corpus.ensure_loaded())
    # print(categorized_corpus.license())
    # print(categorized_corpus.open())
    # print(categorized_corpus.paras())
    # print(categorized_corpus.raw())
    # print(categorized_corpus.readme())
    # print(categorized_corpus.root())
    # print(categorized_corpus.sents())
    # print(categorized_corpus.unicode_repr())
    # print(categorized_corpus.words())
    # print(len(categorized_corpus.words()))

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

    # Get only main words:
    # text = "Hello Hello, how are you my friend?? I'm all good! Thanks :) Just need a leader"
    # text_tokens = word_tokenize(text)
    # print(text_tokens)
    
    # # tokens_without_sw = [word for word in text_tokens if not word in stopwords.words() and word.isalnum()]
    # tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
    # print(tokens_without_sw)

    # # 1: Tokenize the text:
    # text_tokens = word_tokenize(categorized_corpus.raw())
    # print(text_tokens)
    # print("1: Total tokens: ", len(text_tokens))

    # # 2: TODO: Spell checker and corrector here

    # # 3: Make lowercase:
    # tokens_lowercase = list(map(lambda x: x.lower(), text_tokens))
    # print(tokens_lowercase, len(tokens_lowercase))

    # # 4: Remove stop words and special characters:
    # # tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
    # tokens_without_sw = [word for word in tokens_lowercase if not word in stopwords.words("English") and word.isalnum()]
    # print(tokens_without_sw)
    # print("4: Tokens without stopwords and characters: ", len(tokens_without_sw))

    # # 5: Create counter:
    # count = Counter(tokens_without_sw)
    # count = count.most_common()
    # print(*count, sep="\n")
    # print("5: Len count: ", len(count))

    tokens = corpus.tokenize(categorized_corpus.raw())
    tokens_lowercase = corpus.make_lower(tokens)
    tokens_without_sw = corpus.remove_stopwords(tokens_lowercase)
    tokens_without_spec_chars = corpus.remove_spec_chars(tokens_without_sw, log=True)
    


read_corpus()