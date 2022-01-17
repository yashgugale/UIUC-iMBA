
import codecs
import os

from collections import Counter

import nltk
from nltk.corpus.reader.plaintext import CategorizedPlaintextCorpusReader
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag, sent_tokenize, wordpunct_tokenize

import re
from datetime import datetime
import time

# A Zoom chat corpus reader:
class ZoomCorpusReader(CategorizedPlaintextCorpusReader):

    def __init__(self, name, corpus_path):
        self.name = name
        self.corpus_path = corpus_path
        self.cat_pattern = r'(.*)[/]'
        self.doc_pattern = '.*\.txt'
        self.para_interval = 300        # 5 minutes between each comment is considered as a separate section use to create paras


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

    def zoom_chat(self, fileids=None, categories=None):
        """ Return each zoom meeting chat """

        for chat in self.docs(fileids, categories):
            try:
                yield chat
            except Exception as e:
                print("Couldn't retrieve chat data: {}".format(e))
                continue

    def paras(self, fileids=None, categories=None):
        """ Extract all paragraphs in the text """

        for chat in self.zoom_chat(fileids, categories):
            # Find the timestamp:
            results = re.findall('\d{2}:\d{2}:\d{2}', chat)
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
                        idx = chat.find(results[i+1])
                        # print("Index: ", idx)
                        # Return the para till that point:
                        yield chat[start_index:idx]
                        start_index = idx
                # Return the last para:
                yield chat[start_index:]
                start_index = 0

    def sents(self, fileids=None, categories=None):
        """ Extract all sentences from paras """
        
        for paragraph in self.paras(fileids, categories):
            for sentence in sent_tokenize(paragraph):
                yield sentence


    def words(self, fileids=None, categories=None):
        """ Extract all words from sentences """

        # Options for tokenizers in NTLK:
        # TreebankWordTokenizer, WordPunctTokenizer, PunctWordTokenizer, WhitespaceTokenizer
        # Check difference: http://text-processing.com/demo/tokenize/
        for sentence in self.sents(fileids, categories):
            for token in wordpunct_tokenize(sentence):
                yield token

    def tokenize(self, fileids=None, categories=None):
        """ Segments, tokenizes and tags a corpus document """

        for paragraph in self.paras(fileids, categories):
            yield [
                pos_tag(wordpunct_tokenize(sent))
                for sent in sent_tokenize(paragraph)
            ]

    def describe(self, fileids=None, categories=None):
        """ Performs a single pass of the corpus and returns a dictionary with a variety of metrics concerning the state of the corpus."""

        started = time.time()

        # Structures to perform counting:
        counts = nltk.FreqDist()
        tokens = nltk.FreqDist()

        # Perform single pass over paragraphs, tokenize and count:
        for para in self.paras(fileids, categories):
            counts['paras'] += 1

            for sent in sent_tokenize(para):
                counts['sents'] += 1

                for word in wordpunct_tokenize(sent):
                    counts['words'] += 1
                    tokens[word] += 1

        # Compute the number of files and categories in the corpus:
        n_fileids = len(self.resolve(fileids, categories) or self.fileids())
        n_topics = len(self.categories(self.resolve(fileids, categories)))

        # Return data structure with information
        return {
            'files':  n_fileids,
            'topics': n_topics,
            'paras':  counts['paras'],
            'sents':  counts['sents'],
            'words':  counts['words'],
            'vocab':  len(tokens),
            'lexdiv': float(counts['words']) / float(len(tokens)),
            'ppdoc':  float(counts['paras']) / float(n_fileids),
            'sppar':  float(counts['sents']) / float(counts['paras']),
            'secs':   time.time() - started,
        }

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

        
    


