'''
Created on Apr 17, 2015

@author: ruby
'''

from sklearn.cluster import KMeans
from core.dataImporter import importHeadlines
from core.tfIdfHelper import getTfIdfMatrix, getTerms
from core.dataFramesCreator import createTokensFrame, createNewsFrame
from core.clusterInfoProcessor import displayClusterInfo, plotFlatClusterGraph,\
    plotHierarchichalClusterGraph
from categorization.clusterCategorization import categorizeClusters
from data.constants import all_number_of_clusters, createDict, all_categories

number_of_clusters = all_number_of_clusters
number_of_words_per_cluster = 4

# read news headlines, articles
headlines_utf, articles_utf = importHeadlines()
if(headlines_utf.__len__() < articles_utf.__len__()):
    articles_utf = articles_utf[0:headlines_utf.__len__()]

print("Total number of files being clustered %d " % headlines_utf.__len__())
# tf-idf modeling
tf_idf_matrix = getTfIdfMatrix(articles_utf)
terms = getTerms()

# kmeans core, headline->cluster
kMeansObj = KMeans(n_clusters=number_of_clusters)
kMeansObj.fit(tf_idf_matrix)
clusters = kMeansObj.labels_.tolist()
centroids_sorted = kMeansObj.cluster_centers_.argsort()[:, ::-1]  # indices after sort

# create a table of root word->corresponding token: print important words in each cluster
token_frame = createTokensFrame(articles_utf)

# create table of rank, headline, article: print headline
news_frame = createNewsFrame(headlines_utf, articles_utf, clusters)

# display cluster info
clusterInfoList = displayClusterInfo(number_of_clusters, number_of_words_per_cluster, centroids_sorted, token_frame, terms, news_frame)
plotFlatClusterGraph(tf_idf_matrix, clusters, headlines_utf)
plotHierarchichalClusterGraph(tf_idf_matrix, headlines_utf)

#evaluation
print('*****Evaluation*****')
cnt = 0
for cluster in clusterInfoList:
    count = createDict() #{'politics':0,'health':0, 'sports':0, 'entertainment':0}
    headlines = cluster.headlines.split(">##")
    for category in all_categories:
            count[category] = cluster.headlines.count('<'+category)

    print('Cluster '+ str(cnt) + ' size ' + str(headlines.__len__()-1) + str(count))
    cnt += 1
    clusterName = max(count, key=count.get) 
    print("This is a " + clusterName + " cluster")   
# categorization
categorizeClusters(news_frame, number_of_clusters)

    