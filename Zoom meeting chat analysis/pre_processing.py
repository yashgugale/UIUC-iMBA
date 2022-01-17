from collections import Counter
from copyreg import pickle
from ctypes.wintypes import tagMSG
from email.mime import base
from email.policy import default
from pydoc import doc
from textwrap import indent
from tracemalloc import start
from nltk.corpus import stopwords
# Use the following to download the packages to appropirate location:
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk import pos_tag, sent_tokenize, wordpunct_tokenize

import re
import os
from datetime import datetime
import time
import pickle
import json

class PreProcessor(object):
    """
    The preprocessor wraps a corpus object (usually a `ZoomCorpusReader`)
    and manages the stateful tokenization and part of speech tagging into a
    directory that is stored in a format that can be read by the
    `ZoomPickledCorpusReader`. This format is more compact and necessarily
    removes a variety of fields from the document that are stored in the JSON
    representation dumped from the Mongo database. This format however is more
    easily accessed for common parsing activity.
    """
    
    def __init__(self, corpus, target=None, **kwargs):
        """ 
        The corpus is the 'ZoomCorpusReader' to preprocess and pickle.
        The target is the directory on disk to output the pickled corpus to.
        """
        self.corpus = corpus
        self.target = target

    def fileids(self, fileids=None, categories=None):
        """ 
        Access the fileids of the corpus 
        """
        fileids = self.corpus.resolve(fileids, categories)
        if fileids:
            return fileids
        return self.corpus.fileids()

    def abspath(self, fileid):
        """
        Returns the absolute path to the target fileid from the corpus fileid
        """
        # Find the directory, relative to the corpus root:
        parent = os.path.relpath(
            # Using 'self.corpus.corpus_path' instead of 'self.corpus.root':
            os.path.dirname(self.corpus.abspath(fileid)), self.corpus.corpus_path
            # os.path.dirname(self.corpus.abspath(fileid)), self.corpus.root
        )

        # Compute the name parts to reconstruct:
        basename = os.path.basename(fileid)
        name, ext = os.path.splitext(basename)

        # Create the pickle file extension:
        basename = name + '.pickle'

        # Return the path to the file relative to the target:
        return os.path.normpath(os.path.join(self.target, parent, basename))

    def tokenize(self, fileid):
        """
        Segments, tokenizes, and tags a document in the corpus. Returns a
        generator of paragraphs, which are lists of sentences, which in turn
        are lists of part of speech tagged words.
        """
        for paragraph in self.corpus.paras(fileids=fileid):
            yield [
                pos_tag(wordpunct_tokenize(sent))
                for sent in sent_tokenize(paragraph)
            ]

    def process(self, fileid):
        """
        For a single file does the following preprocessing work:
            1. Checks the location on disk to make sure no errors occur.
            2. Gets all paragraphs for the given text.
            3. Segements the paragraphs with the sent_tokenizer
            4. Tokenizes the sentences with the wordpunct_tokenizer
            5. Tags the sentences using the default pos_tagger
            6. Writes the document as a pickle to the target location.
        This method is called multiple times from the transform runner.
        """
        # Compute the outpath to write the file to:
        target = self.abspath(fileid)
        # print("Target: ", target)
        parent = os.path.dirname(target)
        # print("Parent: ", parent)

        # Make sure the directory exists:
        if not os.path.exists(parent):
            print("Directory does not exist. Creating one!")
            os.makedirs(parent)

        # Make sure the parent is a directory and not a file:
        if not os.path.isdir(parent):
            raise ValueError(
                "Please supply a directory to write preprocessed data to."
            )

        # Create a data structure for the pickle:
        document = list(self.tokenize(fileid))
        # print("Document: ", json.dumps(document, indent=4, default="str"))

        # Open and serialize the pickle to disk:
        with open(target, 'wb') as f:
            pickle.dump(document, f, pickle.HIGHEST_PROTOCOL)

        # Clean up the document:
        del document

        # Return the target fileid:
        return target

    def transform(self, fileids=None, categories=None):
        """
        Transform the wrapped corpus, writing out the segmented, tokenized,
        and part of speech tagged corpus as a pickle to the target directory.
        This method will also directly copy files that are in the corpus.root
        directory that are not matched by the corpus.fileids().
        """
        # Make the target directory if it doesn't already exists:
        if not os.path.exists(self.target):
            os.makedirs(self.target)

        # Resolve the fileids to start processing and return the list of
        # target fileids to pass to downstream transformers:
        return [
            self.process(fileid)
            for fileid in self.fileids(fileids, categories)
        ]













class PreProcessing():

    def __init__(self, corpus):
        self.corpus = corpus

    # Old tokenizer function:
    def tokenize_old(self, log=False):
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