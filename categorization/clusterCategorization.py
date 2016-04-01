'''
Created on Apr 26, 2015

@author: ruby
'''
import os
from categorization.textClassifier import nltk_no_stop

cluster_root = '../resources/clusters/'


def categorizeClusters(news_frame, number_of_clusters):
    for i in range(number_of_clusters):
        path = cluster_root+'cluster'+str(i)
        if not os.path.exists(path): os.makedirs(path)
        cnt =1 
        for article in news_frame.ix[i]['article']:
            a_sentence=''
            a_sentence += article
            c_file = open(path+'/c_'+str(cnt)+'.txt',"w")
            c_file.write(a_sentence)
            c_file.close()
            cnt=cnt+1
    
    nltk_no_stop.train()
    nltk_no_stop.performance()
        