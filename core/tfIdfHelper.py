'''
Created on Apr 17, 2015

@author: ruby
'''
from sklearn.feature_extraction.text import TfidfVectorizer

from core.tokenizerAndStemmer import tokenize_and_stem


tf_idf_vectorizer = TfidfVectorizer(lowercase=True, max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1, 3))

def getTfIdfMatrix(articles_utf):
    tf_idf_matrix = tf_idf_vectorizer.fit_transform(articles_utf)
    print(tf_idf_matrix)
    return tf_idf_matrix

def getTerms():
    return tf_idf_vectorizer.get_feature_names()