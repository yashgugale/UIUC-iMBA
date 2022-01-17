from collections import Counter
from nltk.corpus import stopwords
# Use the following to download the packages to appropirate location:
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.tokenize import word_tokenize


class PreProcessing():

    def __init__(self, corpus):
        self.corpus = corpus

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