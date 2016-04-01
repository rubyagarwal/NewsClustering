'''
Created on Apr 17, 2015

@author: ruby
'''

from nltk import SnowballStemmer
import nltk
import re


stemmer = SnowballStemmer("english")

def tokenize(text):
    tokens_all = []
    for sent in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sent):
            tokens_all.append(word)
    
    tokens_words = []
    for t in tokens_all:
        if re.search('[a-zA-Z]', t):
            tokens_words.append(t)
    return tokens_words

def tokenize_and_stem(text):
    tokens_words = tokenize(text)
    tokens_stemmed = []
    for t in tokens_words:
        root = stemmer.stem(t)
        tokens_stemmed.append(root)
    return tokens_stemmed
