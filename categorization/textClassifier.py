'''
Created on Apr 24, 2015

@author: ruby
'''

import re, collections, os
from categorization import naiveBayesObjectCreator as s2
from data.constants import all_number_of_clusters, all_categories, createDict


number_of_clusters = all_number_of_clusters
class text_collection(object):
    pass

news_articles = text_collection()
news_articles.dataFiles = "../resources/dataFiles/"
news_articles.clusters = "../resources/clusters/"
news_articles.categories = all_categories

news_articles.files = dict()
for c in news_articles.categories:
    news_articles.files[c, 'train'] = []
#     news_articles.files[c, 'test'] = []
    
    for f in os.listdir(news_articles.dataFiles + c + "/train/") :
        t_n = news_articles.dataFiles + c + "/train/" + f
        bucket = 'train'
        news_articles.files[c, bucket].append(t_n)

# print(news_articles.files)

def words(filename):
    with open(filename,'r') as f:
        for line in f:
            for word in line.split():
                yield word

class Experiment():
    def train(self):
        training_data = [self.document_features(words(f), c)
                         for c in news_articles.categories
                         for f in news_articles.files[c, 'train']]
        self.model = s2.NB_from_data('category', training_data)
        
    def performance(self):
        print("\n*****Performance:Naive Bayes*****")
        cnt = 0
        for cnt in range(0, number_of_clusters):
            d = createDict()# {'politics':0,'health':0,  'sports':0, 'entertainment':0}
            for f in os.listdir(news_articles.clusters + "cluster" +str(cnt)) :
                path = news_articles.clusters + "cluster" +str(cnt) +"/"+f
                guess = self.model.classify(self.document_features(words(path)))
                d[guess] = d[guess]+1
#                 print(path, guess)
            print("Cluster " + str(cnt) + str(d))

def all_cat_words(cat, train_bucket):
    for f in news_articles.files[cat, train_bucket]:
        for w in words(f):
            yield w

all_words = collections.Counter()
for category in all_categories:
    all_words.update(w for w in all_cat_words(category, 'train'))
# all_words.update(w for w in all_cat_words('politics', 'train'))
# all_words.update(w for w in all_cat_words('health', 'train'))
# all_words.update(w for w in all_cat_words('business', 'train'))
# all_words.update(w for w in all_cat_words('technology', 'train'))
# all_words.update(w for w in all_cat_words('sports', 'train'))
# all_words.update(w for w in all_cat_words('entertainment', 'train'))
nltk_base_words = [w for (w,c) in all_words.most_common(2000)]

def binary_document_features(target_words):
    def encode(document, category=None) :
        document_words = set(document)
        features = {}
        for word in target_words:
            features['contains(%s)' % word] = (word in document_words)
        if category:
            features['category'] = category
        return features
    return encode

nltk_no_stop = Experiment()
stop_word_file = "../resources/stop-word-list.txt"
with open(stop_word_file) as f :
    stop_words = set(line.strip() for line in f)

def candidate_feature_word(w) :
    return w not in stop_words and re.match(r"^[a-z](?:'?[a-z])*$", w) != None

def get_good_items(tokens, t_n) :
    i = 0
    found = 0
    result = []
    while found < t_n and i < len(tokens):
        if candidate_feature_word(tokens[i]) :
            result.append(tokens[i])
            found += 1
        i += 1
    return result

nltk_no_stop_words = get_good_items([w for (w,c) in all_words.most_common()], 2000)
nltk_no_stop.document_features = binary_document_features(nltk_no_stop_words)