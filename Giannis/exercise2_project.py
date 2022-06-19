from random import Random
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from gensim.models import Word2Vec,word2vec
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import re
import logging
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import os
from sklearn.cluster import KMeans


df = pd.read_csv("amazon.csv")

text=[]
scores=[]

# for i in range(len(df)):
#     text.append(df["Text"][i])
#     scores.append(df["Score"][i])

# #Test and Train Data
# train_features,test_features,train_labels,test_labels = train_test_split(text,scores,test_size = 0.2,random_state = 42)

# for i in range(len(train_labels)):
#     if train_labels[i] >=3:
#         train_labels[i]=1
#     else:
#         train_labels[i]=0

# for i in range(len(test_labels)):
#     if test_labels[i] >=3:
#         test_labels[i]=1
#     else:
#         test_labels[i]=0

# #BAG OF WORDS
# print("Using Vectorizer")
# from sklearn.feature_extraction.text import CountVectorizer


# def text_to_words(review):
#     review_text = re.sub("[^a-zA-Z]"," ", review)
#     words = review_text.lower().split()
#     stops = set(stopwords.words("english"))
#     words = [w for w in words if not w in stops]
#     return (" ".join(words))

# #Train Data
# cleaned_train_reviews = []
# for i in range(len(train_features)):
#     cleaned_train_reviews.append(text_to_words(train_features[i]))

# #Creating Features from a Bag of Words
# vectorizer = CountVectorizer(analyzer = "word",
#                             tokenizer = None,
#                             preprocessor = None,
#                             stop_words = None,
#                             max_features = 10000
#                             )

# train_data_features = vectorizer.fit_transform(cleaned_train_reviews)
# train_data_features = train_data_features.toarray()
# print(train_data_features.shape)

# # vocabulary = vectorizer.get_feature_names()
# #Test Data
# cleaned_test_reviews = []
# for i in range(len(test_features)):
#     cleaned_test_reviews.append(text_to_words(test_features[i]))


# test_data_features = vectorizer.fit_transform(cleaned_test_reviews)
# test_data_features = test_data_features.toarray()
# print(test_data_features.shape)


# #RandomForest
# print("Training the random forest....")
# model = RandomForestClassifier(n_estimators=100)
# print(1)
# model = model.fit(train_data_features,train_labels)
# print(2)
# result = model.predict(test_data_features)
# print(3)
# print(result)
# print("CANCUN")
# print("Accuracy")
# errors=0
# for i in range(len(test_labels)):
#     print(i,test_features[i],test_labels[i],result[i])

# print(errors,errors/10000)


#Word2Vec
for i in range(len(df)):
    text.append(df["Text"][i])
    scores.append(df["Score"][i])

#Test and Train Data
train_features,test_features,train_labels,test_labels = train_test_split(text,scores,test_size = 0.2,random_state = 42)

for i in range(len(train_labels)):
    if train_labels[i] >=3:
        train_labels[i]=1
    else:
        train_labels[i]=0

for i in range(len(test_labels)):
    if test_labels[i] >=3:
        test_labels[i]=1
    else:
        test_labels[i]=0

print("Using Word2Vec")
def text_to_wordlist(review,remove_stopwords):
    review_text = re.sub("[^a-zA-Z]"," ", review)
    words = review_text.lower().split()
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
    return words

import nltk.data
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def review_to_sentences(review,tokenizer,remove_stopwords=False):
    raw_sentences = tokenizer.tokenize(review.strip())
    sentences = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence)>0:
            sentences.append(text_to_wordlist(raw_sentence,remove_stopwords))
    return sentences


sentences = []
print ("Parsing sentences from training set")

for review in train_features:
    sentences += review_to_sentences(review,tokenizer)

print ("Parsing sentences from unlabeled set")
for review in test_features:
    sentences += review_to_sentences(review,tokenizer)

num_features = 300
min_word_count = 10
num_workers = 4
downsampling = 1e-3
context = 10

print("Training Model")

model = word2vec.Word2Vec(sentences,workers = num_workers,vector_size = num_features,min_count = min_word_count,window = context, sample = downsampling)

model_name = 'train-model'
model.save(model_name)

clean_train_reviews = [] 
for review in train_features:
    clean_train_reviews.append(text_to_wordlist(review,remove_stopwords=True))

clean_test_reviews = [] 
for review in test_features:
    clean_test_reviews.append(text_to_wordlist(review,remove_stopwords=True))


#Vectors averaging

# def makeFeatureVec(words,model,num_features):
#     featureVec = np.zeros((num_features,),dtype="float32")
#     num_words = 0
#     index2word_set = set(model.wv.index_to_key)
#     for word in words:
#         if word in index2word_set:
#             num_words +=1
#             featureVec = np.add(featureVec,model.wv[word])
#     if num_words==0:
#         num_words=1
#     featureVec = np.divide(featureVec,num_words)
#     return featureVec

# def getAverageFeatureVecs(reviews,model,num_features):
#     counter = 0 
#     reviewFeatureVecs = np.zeros((len(reviews),num_features),dtype="float32")
#     for review in reviews:
#         print( "Review %d of %d" % (counter, len(reviews)))
#         reviewFeatureVecs[counter] = makeFeatureVec(review,model,num_features)
#         counter = counter + 1
#     return reviewFeatureVecs

# print("Creating average feature vecs for train reviews")
# trainDataVecs = getAverageFeatureVecs(clean_train_reviews,model,num_features)

# print("Creating average feature vecs for test reviews")
# testDataVecs = getAverageFeatureVecs(clean_test_reviews,model,num_features)


# print("Randdom Forest ")
# forest = RandomForestClassifier(n_estimators=100)


# print ("Fitting a random forest to labeled training data...")

# forest = forest.fit(trainDataVecs,train_labels)

# result = forest.predict(testDataVecs)


# print("Accuracy")
# errors=0
# for i in range(len(test_labels)):
#     if test_labels[i]!=result[i]:
#         errors+=1
#         print(i,test_features[i],test_labels[i],result[i])
# print(errors,errors/10000)




#Clustering
import time

print("Kmeans Clustering of words in model")
start = time.time()
word_vectors = model.wv.vectors
num_clusters = int(word_vectors.shape[0]/5)
print("Start")
kmeans_clustering = KMeans(n_clusters = num_clusters)
idx = kmeans_clustering.fit_predict(word_vectors)

end = time.time()
print("End of clustering")
print("Took Time {}".format(end-start))

#mapping each word to a cluster
word_centroid_map = dict(zip(model.wv.index_to_key,idx))

word_centroid_keys = list(word_centroid_map.keys())
word_centroid_val = list(word_centroid_map.values())
print(word_centroid_keys)
print("sfdsfdsfdsfsdsdffsdfdsfsdffffffffffffssssssssssssssssssss")
print(word_centroid_val)

# print("For the first 10 clusters")

# for cluster in range(0,10):
#     print("Cluster number {}".format(cluster))
#     words = []
#     for i in range(len(word_centroid_val)):
#         if word_centroid_val[i]==cluster:
#             words.append(word_centroid_keys[i])
#     print(words)


def create_bag_of_centroids(wordlist,word_centroid_keys,word_centroid_val):
    num_centroids = max(word_centroid_val)+1
    bag_of_centroids = np.zeros(num_centroids,dtype="float32")
    for word in wordlist:
        if word in word_centroid_keys:
            index = word_centroid_map[word]
            bag_of_centroids[index]+=1
    return bag_of_centroids


train_centroids = np.zeros((len(train_features),num_clusters),dtype="float32")

counter=0
for review in clean_train_reviews:
    train_centroids[counter] = create_bag_of_centroids(review,word_centroid_keys,word_centroid_val)
    counter+=1

counter=0
test_centroids = np.zeros((len(test_features),num_clusters),dtype="float32")
for review in clean_test_reviews:
    test_centroids[counter] = create_bag_of_centroids(review,word_centroid_keys,word_centroid_val)
    counter+=1

#Random Forest
forest = RandomForestClassifier(n_estimators = 100)
print ("Fitting a random forest to labeled training data...")
forest = forest.fit(train_centroids,train_labels)
result = forest.predict(test_centroids)

print("Accuracy")
errors=0
for i in range(len(test_labels)):
    if test_labels[i]!=result[i]:
        errors+=1
        print(i,test_features[i],test_labels[i],result[i])
print(errors,errors/10000)

