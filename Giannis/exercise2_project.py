import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from gensim.models import word2vec
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score,precision_score,recall_score, confusion_matrix
import re
from nltk.corpus import stopwords
import os
from sklearn.cluster import KMeans
import nltk.data
import seaborn as sns

directory=os.getcwd()

##Αφού φορτώσουμε τα δεδομένα στο πρόγραμμά μας, δημιουργούμε τα κατάλληλα train και test data με αναλογία 80%-20% για την
##εκπαίδευση του συστήματός μας.

df = pd.read_csv("amazon.csv")

text=[]
scores=[]

for i in range(len(df)):
    text.append(df["Text"][i])
    scores.append(df["Score"][i])

##A graph for scores 1-5
labels=[1,2,3,4,5]
reviews=[0,0,0,0,0]
for j in range(len(scores)):
    reviews[scores[j]-1]+=1

plt.bar(x=labels,height=reviews,tick_label=labels,width=0.8,color=['red','green','blue','yellow','grey'])
plt.xlabel('Review rates')
plt.ylabel('Reviews')
plt.title("Number of review-scores")
plt.show()

##A graph of scores positive-negative
x=[1,2]
labels=["positive","negative"]
reviews=[0,0]
for j in range(len(scores)):
    if scores[j]>=3:
        reviews[0]+=1
    else:
        reviews[1]+=1

plt.bar(x=x,height=reviews,tick_label=labels,width=0.8,color=['red','green'])
plt.xlabel('Review rates')
plt.ylabel('Reviews')
plt.title("Number of review-scores")
plt.show()


##A graph of scores positive-neutral-negative
x=[1,2,3]
labels=['positive','neutral','negative']
reviews=[0,0,0]
for j in range(len(scores)):
    if scores[j]>3:
        reviews[0]+=1
    elif scores[j]<3:
        reviews[2]+=1
    else:
        reviews[1]+=1

plt.bar(x=labels,height=reviews,tick_label=labels,width=0.8,color=['red','green','blue'])
plt.xlabel('Review rates')
plt.ylabel('Reviews')
plt.title("Number of review-scores")
plt.show()

##Διαλέγουμε κατηγοριοποίηση σε περίπτωση που δεν θέλουμε τα σκορ απο 1-5

###For positive and negative reviews
# for i in range(len(scores)):
#     if scores[i]>=3:
#         scores[i]="positive"
#     else:
#         scores[i]="negative"


##For positive,negative and neutral reviews
# for i in range(len(scores)):
#     if scores[i] >3:
#         scores[i]="positive"
#     elif scores[i] == 3:
#         scores[i]="neutral"
#     else:
#         scores[i]="negative"




##Αφού κάνουμε μία μικρή προεπεξεργασία στα δεδομένα μας, βγάζοντας λέξεις όπως is,are και σημεία στίξης από τα κείμενα και φτιάχνοντας λίστες λέξεων για κάθε μία πρόταση κάθε review,
##μετατρέπουμε τα κείμενα των reviews σε διανύσματα με την τεχνική των Word Embeddings μέσω της βιβλιοθήκης Word2Vec της python
##και εκπαιδεύουμε το μοντέλο μας.

print("Using Word2Vec")

def text_to_wordlist(review,remove_stopwords):
    review_text = re.sub("[^a-zA-Z]"," ", review)
    words = review_text.lower().split()
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
    return words


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

##Σπάμε το review σε προτάσεις
def review_to_sentences(review,tokenizer,remove_stopwords=False):
    raw_sentences = tokenizer.tokenize(review.strip())
    sentences = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence)>0:
            sentences.append(text_to_wordlist(raw_sentence,remove_stopwords))
    return sentences


sentences = []
print ("Parsing sentences")

for review in text:
    sentences += review_to_sentences(review,tokenizer)

##Παράμετροι του μοντέλου μας
num_features = 300 #Μέγεθος διανύσματος κάθε λέξης
min_word_count = 10 ##Minimum word count
num_workers = 4 ##Number of threads to run in parallel
downsampling = 1e-3 ##Downsample setting for frequent words
context = 10  ##context window size

print("Training Model")
##Εκπαίδευση του μοντέλου Word Embeddings
model = word2vec.Word2Vec(sentences,workers = num_workers,vector_size = num_features,min_count = min_word_count,window = context, sample = downsampling)

model_name = 'trainmodel'
model.save(model_name)

# ##Πριν φτιάξουμε το Random Forest, θα πρέπει να εκφράσουμε κάθε ένα review με έναν τρόπο το οποίο θα παίρνει σαν είσοδο το Random Forest και μέσω αυτού θα προβλέπει
# ##την κριτική του χρήστη. Εδώ εφαρμόζουμε δύο τεχνικές:
# # - Στη πρώτη παίρνουμε το "μέσο" vector κάθε review (Vectors Averaging) αθροίζοντας τα vectors κάθε λέξης που το απαρτίζουν(εφόσον υπάρχει στο μοντέλο) και διαιρώντας το άθροισμα στη συνέχεια με τον αριθμό των λέξεων
# # - Στη δεύτερη χρησιμοποιούμε Kmeans αλγόριθμο για να ομαδοποιήσουμε τις λέξεις του μοντέλου μας σε clusters και στη συνέχεια φτιάχνουμε ένα vector διάστασης όσα και τα clusters για κάθε ένα review 
# # όπου και καταγράφουμε τις φορές που λέξεις του review υπάρχουν σε ένα cluster (Clustering).


print("Loading model")
# model =  load_model('{}/trainmodel'.format(directory))

num_features = 300 

# #Vectors averaging
def makeFeatureVec(words,model,num_features):
    featureVec = np.zeros((num_features,),dtype="float32")
    num_words = 0
    index2word_set = set(model.wv.index_to_key)
    for word in words:
        if word in index2word_set:
            num_words +=1
            featureVec = np.add(featureVec,model.wv[word])
    if num_words==0:
        num_words=1
    featureVec = np.divide(featureVec,num_words)
    return featureVec

def getAverageFeatureVecs(reviews,model,num_features):
    counter = 0 
    reviewFeatureVecs = np.zeros((len(reviews),num_features),dtype="float32")
    for review in reviews:
        reviewFeatureVecs[counter] = makeFeatureVec(review,model,num_features)
        counter = counter + 1
    return reviewFeatureVecs

print("Creating average feature vecs for reviews")
DataVecs = getAverageFeatureVecs(text,model,num_features)

print(len(DataVecs))


#Test and Train Data
train_features,test_features,train_labels,test_labels = train_test_split(DataVecs,scores,test_size = 0.2,random_state = 42)


##Δημιουργία του Random Forest. Αφού εκπαιδεύσουμε το σύστημα με τα "φτιαγμένα" training data, εφαρμόζουμε τα "φτιαγμένα" test data
print("Random Forest")
forest = RandomForestClassifier(n_estimators=100) ## χρησιμοποιούμε 100 trees

print ("Fitting a random forest to labeled training data...")

forest = forest.fit(train_features,train_labels)

result = forest.predict(test_features)

errors=0

for i in range(len(test_labels)):
    if test_labels[i]!=result[i]:
        errors+=1
        # print(i,test_features[i],test_labels[i],result[i])
print("Accuracy {:.2f}%".format( (1 - (errors/10000))*100)) ##accuracy
print("Precision score = {}".format(precision_score(test_labels,result,average=None))) ##precision per classification
print("Recall score = {}".format(recall_score(test_labels,result,average=None)))##recall per classification
print("F1 score = {}".format(f1_score(test_labels,result,average=None)))##f1 score
cf_matrix = confusion_matrix(test_labels,result)
ax = sns.heatmap(cf_matrix,annot=True,cmap="Blues")
ax.set_title('Confusion Matrix of Reviews\n\n');
ax.set_xlabel('\nPredicted Values')
ax.set_ylabel('Actual Values')

######Ανάλογα τη κατηγοριοποίηση

# ax.xaxis.set_ticklabels(['Positive','Neutral','Negative'])
# ax.yaxis.set_ticklabels(['Positive','Neutral','Negative'])

# ax.xaxis.set_ticklabels(['Positive','Negative'])
# ax.yaxis.set_ticklabels(['Positive','Negative'])

ax.xaxis.set_ticklabels(['1','2','3','4','5'])
ax.yaxis.set_ticklabels(['1','2','3','4','5'])

plt.show()


#Clustering

print("Loading model")
# model = keras.models.load_model('trainmodel')

def text_to_wordlist(review,remove_stopwords):
    review_text = re.sub("[^a-zA-Z]"," ", review)
    words = review_text.lower().split()
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
    return words


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

##Σπάμε το review σε προτάσεις
def review_to_sentences(review,tokenizer,remove_stopwords=False):
    raw_sentences = tokenizer.tokenize(review.strip())
    sentences = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence)>0:
            sentences.append(text_to_wordlist(raw_sentence,remove_stopwords))
    return sentences


print("Kmeans Clustering of words in model")
word_vectors = model.wv.vectors
num_clusters = int(word_vectors.shape[0]/5) ##cluster number is the 1/5th of the vocabulary size or an of average 5 words per cluster
kmeans_clustering = KMeans(n_clusters = num_clusters)
idx = kmeans_clustering.fit_predict(word_vectors)


#mapping each word to a cluster
word_centroid_map = dict(zip(model.wv.index_to_key,idx))

word_centroid_keys = list(word_centroid_map.keys())
print(11)
word_centroid_val = list(word_centroid_map.values())


def create_bag_of_centroids(wordlist,word_centroid_keys,word_centroid_val):
    num_centroids = max(word_centroid_val)+1
    bag_of_centroids = np.zeros(num_centroids,dtype="float32")
    for word in wordlist:
        if word in word_centroid_keys:
            index = word_centroid_map[word]
            bag_of_centroids[index]+=1
    return bag_of_centroids


clean_reviews = [] 
for review in text:
    clean_reviews.append(text_to_wordlist(review,remove_stopwords=True))

centroids = np.zeros((len(text),num_clusters),dtype="float32")
counter=0
for review in clean_reviews:
    centroids[counter] = create_bag_of_centroids(review,word_centroid_keys,word_centroid_val)
    counter+=1

print(len(centroids))
# counter=0
# test_centroids = np.zeros((len(test_features),num_clusters),dtype="float32")
# for review in clean_test_reviews:
#     test_centroids[counter] = create_bag_of_centroids(review,word_centroid_keys,word_centroid_val)
#     counter+=1

#Δημιουργία του Random Forest. Αφού εκπαιδεύσουμε το σύστημα με τα "φτιαγμένα" training data, εφαρμόζουμε τα "φτιαγμένα" test data
#Random Forest

train_features,test_features,train_labels,test_labels = train_test_split(centroids,scores,test_size = 0.2,random_state = 42)


forest = RandomForestClassifier(n_estimators = 100)
print ("Fitting a random forest to labeled training data...")
forest = forest.fit(train_features,train_labels)
result = forest.predict(test_features)

errors=0
for i in range(len(test_labels)):
    if test_labels[i]!=result[i]:
        errors+=1
print("Accuracy {:.2f}%".format( (1 - (errors/10000))*100)) ##accuracy
print("Precision score = {}".format(precision_score(test_labels,result,average=None))) ##precision per classification
print("Recall score = {}".format(recall_score(test_labels,result,average=None)))##recall per classification
print("F1 score = {}".format(f1_score(test_labels,result,average=None)))##f1 score
cf_matrix = confusion_matrix(test_labels,result)
ax = sns.heatmap(cf_matrix,annot=True,cmap="Blues")
ax.set_title('Seaborn Confusion Matrix with labels\n\n');
ax.set_xlabel('\nPredicted Values')
ax.set_ylabel('Actual Values')

#####Ανάλογα τη κατηγοριοποίηση
# ax.xaxis.set_ticklabels(['Positive','Neutral','Negative'])
# ax.yaxis.set_ticklabels(['Positive','Neutral','Negative'])

# ax.xaxis.set_ticklabels(['Positive','Negative'])
# ax.yaxis.set_ticklabels(['Positive','Negative'])

ax.xaxis.set_ticklabels(['1','2','3','4','5'])
ax.yaxis.set_ticklabels(['1','2','3','4','5'])

plt.show()


