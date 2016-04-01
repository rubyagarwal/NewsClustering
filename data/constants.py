
'''
Created on Apr 26, 2015

@author: ruby
'''

all_number_of_clusters = 6
all_categories = ['politics','health', 'sports','entertainment', 'business', 'technology']

def createDict():
    d = {}
    for category in all_categories:
        d[category]= 0
    return d