'''
Created on Apr 24, 2015

@author: ruby
'''

import os
from data.constants import all_number_of_clusters, all_categories

category_cnt = all_number_of_clusters

data_loc = '../resources/dataFiles/'
categories = all_categories

for c in categories:
    articles = open('../resources/news/'+c+'.txt').read().split('\n BREAKS HERE')
    headlines = open('../resources/headlines/'+c+'.txt').read().split('\n')
    
    total_cnt = 120
    num = 5
    den = 6
    train_cnt = total_cnt*num/den #((headlines.__len__() * 8)/10)
    print(train_cnt)
    
    test_cnt = total_cnt - train_cnt
    # create folder category
    newpath = data_loc+c
    if not os.path.exists(newpath): os.makedirs(newpath)
    print(newpath)

    trainpath = newpath + "/train/"
    if not os.path.exists(trainpath): os.makedirs(trainpath)
    
    testpath = newpath + "/test/"
    if not os.path.exists(testpath): os.makedirs(testpath)
    
    cnt = 1
    for a in articles:
        if a:
            if cnt <=total_cnt:
                #if cnt <= train_cnt:
                if (cnt % den) !=0:
                    train_file = open(trainpath+"/n_"+str(cnt)+'.txt', "w")
                    train_file.write(headlines[cnt-1])
                    train_file.write("\nHEADLINE_ARTICLE\n")
                    train_file.write(a)
                    train_file.close()
                #elif cnt <= (train_cnt + test_cnt):
                else:
                    test_file = open(testpath+"/n_"+str(cnt)+'.txt', "w")
                    test_file.write('<'+c+'>##'+headlines[cnt-1])
                    test_file.write("\nHEADLINE_ARTICLE\n")
                    test_file.write(a)
                    test_file.close() 
                cnt = cnt +1