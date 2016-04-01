'''
Created on Apr 17, 2015

@author: ruby
'''

import os
from data.constants import all_number_of_clusters, all_categories

category_cnt = all_number_of_clusters
categories = all_categories
root = '../resources/dataFiles/'

def importHeadlines():
    headlines_utf = []
    articles_utf = []
    for c in categories:
        for f in os.listdir(root + c + "/test/") :
            path = root + c + "/test/" + f
            h = open(path).read().split('\nHEADLINE_ARTICLE\n')
            if (h and h[0] and h[1]):
                headline = unicode(h[0], 'utf-8')
                article = unicode(h[1], 'utf-8')
                headlines_utf.append(headline)
                articles_utf.append(article)
#     print(headlines_utf)
#     print(headlines_utf.__len__())
#     print(articles_utf)
#     print(articles_utf.__len__())
    return headlines_utf, articles_utf