'''
Created on Apr 17, 2015

@author: ruby
'''

import pandas

from core.tokenizerAndStemmer import tokenize, tokenize_and_stem


all_articles_tokenized = []
all_articles_stemmed = []

# for every article, find tokens. For every token find the root word
def populateLists(articles_utf):
    for a in articles_utf:
        tokens = tokenize(a)
        all_articles_tokenized.extend(tokens)
    
        stems = tokenize_and_stem(a)
        all_articles_stemmed.extend(stems)

def createTokensFrame(articles_utf):
    populateLists(articles_utf)
    data_frame = pandas.DataFrame({'words':all_articles_tokenized}, index=all_articles_stemmed)
    return data_frame

def getRanks(count):
    ranks = []
    for r in range(0, count):
        ranks.append(r)
    return ranks

# create table of rank, headline, article->print headline
def createNewsFrame(headlines_utf, articles_utf,clusters):
    ranks = getRanks(len(headlines_utf))
    news = {'headline':headlines_utf, 'article':articles_utf, 'cluster':clusters, 'rank':ranks}
    news_frame = pandas.DataFrame(news, index=[clusters], columns=['rank', 'headline', 'article'])
    return news_frame