'''
Created on Apr 17, 2015

@author: ruby
'''

import pandas
from scipy.cluster.hierarchy import ward, dendrogram
from sklearn.manifold import MDS
from sklearn.metrics.pairwise import cosine_similarity

import matplotlib.pyplot as plt
from data.ClusterInfo import ClusterInfo


def displayClusterInfo(number_of_clusters, number_of_words_per_cluster, centroids_sorted, token_frame, terms, news_frame):
    clusterInfoList=[]
    print('*****Analysis of clusters:*****')
    for t_n in range(number_of_clusters):
        print(" Cluster %d " % t_n)
        important_words = 'Words: '
        for i in centroids_sorted[t_n, :number_of_words_per_cluster]:
            important_words += (token_frame.ix[terms[i].split(' ')].values.tolist()[0][0])
            important_words += (", ")
#         print("%s " % important_words)
        
        cluster_headlines = 'Headlines: '
        for headline in news_frame.ix[t_n]['headline']:
            h_sentence=''
            h_sentence += headline
            cluster_headlines += h_sentence
            cluster_headlines += (", ")
        print("%s " % cluster_headlines)
        clusterInfo = ClusterInfo(important_words,cluster_headlines)
        clusterInfoList.append(clusterInfo)
    return clusterInfoList

def plotFlatClusterGraph(tf_idf_matrix, clusters, headlines_utf):
    dist = 1 - cosine_similarity(tf_idf_matrix)
    MDS()
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
    pos = mds.fit_transform(dist)
    xs, ys = pos[:, 0], pos[:, 1]
    cluster_colors = {0: '#FE642E', 1: '#B40404', 2: '#D7DF01', 3: '#01DF01', 4: '#00FFBF', 5: '#2E64FE', 6:'#8904B1', 7:'#FA58F4', 8:'#FE2E9A', 9:'#A4A4A4'}

    #create data frame that has the result of the MDS plus the cluster numbers and titles
    df = pandas.DataFrame(dict(x=xs, y=ys, label=clusters, title=headlines_utf)) 
    groups = df.groupby('label')

    # set up plots
    fig, ax = plt.subplots(figsize=(17, 9)) # set size

    #iterate through groups to layer the plots
    for name, group in groups:
        ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, color=cluster_colors[name], mec='none')
        ax.set_aspect('auto')
        ax.tick_params(axis= 'x', which='both', bottom='off', top='off', labelbottom='off')
        ax.tick_params(axis= 'y', which='both', left='off', top='off', labelleft='off')
        ax.legend(numpoints=1)  #show legend with only 1 point

    #add label in x,y position with the label as the film title
    for t_n in range(len(df)):
        ax.text(df.ix[t_n]['x'], df.ix[t_n]['y'], df.ix[t_n]['title'], size=8)  
    
    plt.savefig('../plots/flat_clusters.png', dpi=400)
    
def plotHierarchichalClusterGraph(tf_idf_matrix, headlines_utf):
    dist = 1 - cosine_similarity(tf_idf_matrix)
    linkage_matrix = ward(dist)
    fig, ax = plt.subplots(figsize=(15, 20)) # set size
    dendrogram(linkage_matrix, orientation="right", labels=headlines_utf);

    plt.tick_params(axis= 'x', which='both', bottom='off', top='off', labelbottom='off')
    plt.tight_layout()
    plt.savefig('../plots/hierachichal_clusters.png', dpi=200) 