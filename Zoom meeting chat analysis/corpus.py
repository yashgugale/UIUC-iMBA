
import codecs
import os

from nltk.corpus.reader.plaintext import CategorizedPlaintextCorpusReader

from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class ZoomCorpus(CategorizedPlaintextCorpusReader):

    def __init__(self, name, corpus_path):
        self.name = name
        self.corpus_path = corpus_path
        self.cat_pattern = r'(.*)[/]'
        self.doc_pattern = '.*\.txt'

        CategorizedPlaintextCorpusReader.__init__(self, 
            self.corpus_path, 
            self.doc_pattern, 
            cat_pattern=self.cat_pattern)

    def resolve(self, fileids, categories):
        """
        Returns a list of fileids or categories depending on what is passed
        to each internal corpus reader function. Implemented similarly to
        the NLTK ``CategorizedPlaintextCorpusReader``.
        """
        if fileids is not None and categories is not None:
            raise ValueError("Specify fileids or categories, not both")

        if categories is not None:
            return self.fileids(categories)
        return fileids

    def docs(self, fileids=None, categories=None):
        """
        Returns the complete text of a document, closing the document
        after we are done reading it and yielding it in a memory safe fashion.
        """
        # Resolve the fileids and the categories
        fileids = self.resolve(fileids, categories)

        # Create a generator, loading one document into memory at a time.
        for path, encoding in self.abspaths(fileids, include_encoding=True):
            with codecs.open(path, 'r', encoding=encoding) as f:
                yield f.read()

    def sizes(self, fileids=None, categories=None):
        """
        Returns a list of tuples, the fileid and size on disk of the file.
        This function is used to detect oddly large files in the corpus.
        """
        # Resolve the fileids and the categories
        fileids = self.resolve(fileids, categories)

        # Create a generator, getting every path and computing filesize
        for path in self.abspaths(fileids):
            yield os.path.getsize(path)

    # # Read a categorized plain text corpus:
    # def categorized_plain_text_corpus_reader(self):

    #     # Read the corpus:
    #     corpus = CategorizedPlaintextCorpusReader(
    #         self.corpus_path, self.doc_pattern, cat_pattern=self.cat_pattern
    #     )
    #     self.corpus = corpus

    #     return corpus

    # def tokenize(self, log=False):
    #     """ Tokenize the text """
    #     text_tokens = word_tokenize(self.raw())
    #     if(log):
    #         print(text_tokens)
    #         print("1: Total tokens: ", len(text_tokens))

    #     self.text_tokens = text_tokens
    #     return text_tokens

    # def make_lower(self, tokens, log=False):
    #     """ Make tokens lowercase """
    #     tokens_lowercase = list(map(lambda x: x.lower(), tokens))
    #     if(log):
    #         print(tokens_lowercase)
    #         print("Tokens lower: ", len(tokens_lowercase))

    #     self.tokens_lowercase = tokens_lowercase
    #     return tokens_lowercase

    # def remove_stopwords(self, tokens, log=False):
    #     """ Remove stopwords from tokens """
    #     tokens_without_sw = [word for word in tokens if not word in stopwords.words("English")]
    #     if(log):
    #         print(tokens_without_sw)
    #         print("Tokens without stopwords: ", len(tokens_without_sw))

    #     self.tokens_without_sw = tokens_without_sw
    #     return tokens_without_sw

    # def remove_spec_chars(self, tokens, log=False):
    #     """ Remove tokens with special characters """
    #     tokens_without_spec_chars = [word for word in tokens if word.isalnum()]
    #     if(log):
    #         print(tokens_without_spec_chars)
    #         print("Tokens without special characters: ", len(tokens_without_spec_chars))

    #     self.tokens_without_spec_chars = tokens_without_spec_chars
    #     return tokens_without_spec_chars

    # def spell_check(self, tokens, log=False):
    #     """ Spell checker """
    #     # TODO: Spell checker and corrector here
    #     pass

        
    


