'''
Created on Apr 23, 2015

@author: ruby
'''

class ClusterInfo:
    importantWords = ""
    headlines = ""
    
    def __init__(self, words, headlines):
        self.importantWords = words
        self.headlines = headlines  