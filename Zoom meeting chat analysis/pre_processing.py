from collections import Counter
from tracemalloc import start
from nltk.corpus import stopwords
# Use the following to download the packages to appropirate location:
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk import sent_tokenize
from nltk import wordpunct_tokenize

import re
from datetime import datetime

class PreProcessing():

    def __init__(self, corpus):
        self.corpus = corpus
        self.para_interval = 300        # 5 minutes between each comment is considered as a separate section use to create paras

    def paras(self):
        """ Extract all paragraphs in the text """

        # Find the timestamp:
        results = re.findall('\d{2}:\d{2}:\d{2}', self.corpus.raw())
        if(results):
            start_index = 0
            for i in range(len(results)-1):
                t1 = datetime.strptime(results[i], '%H:%M:%S')
                t2 = datetime.strptime(results[i+1], '%H:%M:%S')
                diff = (t2 - t1).total_seconds()
                # If the diference between two timestamps is more than 5 mins, we have found a new para:
                if(diff > self.para_interval):
                    # print(diff)
                    # print(results[i+1])
                    idx = self.corpus.raw().find(results[i+1])
                    # print("Index: ", idx)
                    # Return the para till that point:
                    yield self.corpus.raw()[start_index:idx]
                    start_index = idx
            # Return the last para:
            yield self.corpus.raw()[start_index:]

    def sents(self):
        """ Extract all sentences from paras """
        
        for paragraph in self.paras():
            for sentence in sent_tokenize(paragraph):
                yield sentence

    def words(self):
        """ Extract all words from sentences """
        # Options for tokenizers in NTLK:
        # TreebankWordTokenizer, WordPunctTokenizer, PunctWordTokenizer, WhitespaceTokenizer
        # Check difference: http://text-processing.com/demo/tokenize/
        for sentence in self.sents():
            for token in wordpunct_tokenize(sentence):
                yield token

    def tokenize(self, log=False):
        """ Tokenize the text """

        text_tokens = word_tokenize(self.corpus.raw())
        if(log):
            print(text_tokens)
            print("1: Total tokens: ", len(text_tokens))

        self.text_tokens = text_tokens
        return text_tokens

    def make_lower(self, tokens, log=False):
        """ Make tokens lowercase """

        tokens_lowercase = list(map(lambda x: x.lower(), tokens))
        if(log):
            print(tokens_lowercase)
            print("Tokens lower: ", len(tokens_lowercase))

        self.tokens_lowercase = tokens_lowercase
        return tokens_lowercase

    def remove_stopwords(self, tokens, log=False):
        """ Remove stopwords from tokens """

        tokens_without_sw = [word for word in tokens if not word in stopwords.words("English")]
        if(log):
            print(tokens_without_sw)
            print("Tokens without stopwords: ", len(tokens_without_sw))

        self.tokens_without_sw = tokens_without_sw
        return tokens_without_sw

    def remove_spec_chars(self, tokens, log=False):
        """ Remove tokens with special characters """

        tokens_without_spec_chars = [word for word in tokens if word.isalnum()]
        if(log):
            print(tokens_without_spec_chars)
            print("Tokens without special characters: ", len(tokens_without_spec_chars))

        self.tokens_without_spec_chars = tokens_without_spec_chars
        return tokens_without_spec_chars

    def spell_check(self, tokens, log=False):
        """ Spell checker """

        # TODO: Spell checker and corrector here
        pass