from sklearn.cluster import KMeans
from pandas import DataFrame
import sys, codecs, numpy
import numpy as np
import argparse
import logging
import time
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from utils import *
from wordCluster import *


# load the word to vector model
start = time.time()
print("Load word2vec model ... ", end="", flush=True)
model_path='data/GoogleNews-vectors-negative300.bin'
w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=bool(1))
print("finished in {:.2f} sec.".format(time.time() - start), flush=True)
word_vectors = w2v_model.wv.syn0
n_words = word_vectors.shape[0]
vec_size = word_vectors.shape[1]
print("#words = {0}, vector size = {1}".format(n_words, vec_size))


# get the labels, and vectors for each label
array=[]
with open('data/all_predicate.txt', 'r') as myfile:
    array=[]
    for line in myfile:
        *others, last = line.split('/')
        last=last.rstrip('\n') 
        array.append(last)
        
with open('data/all_predicate_entity.txt', mode='wt', encoding='utf-8') as myfile:
    myfile.write('\n'.join(array))


#make cluster among all the predicts
labels_array = []
numpy_arrays = []
for entity in array:
    labels_array.append(entity)
    sr = phrase_vector(entity, w2v_model)
    numpy_arrays.append(np.array([float(i) for i in sr[0:]]) )
numpy_arrays = np.array( numpy_arrays )

numOfCluster=52
print("clustering in {} groups \n".format(numOfCluster))
kmeans_model = KMeans(init='k-means++', n_clusters=numOfCluster, n_init=10)
kmeans_model.fit(numpy_arrays)
cluster_labels  = kmeans_model.labels_
cluster_inertia   = kmeans_model.inertia_
cluster_to_words  = find_word_clusters(labels_array, cluster_labels)


# Give a word for each cluster
most_similar_words=[]
for i in range(0, numOfCluster):
    #print(i)
    model_word_vector = np.array(kmeans_model.cluster_centers_[i], dtype='f')
    similar_word = w2v_model.most_similar( [ model_word_vector ], [], topn=1)[0][0]  
    most_similar_words.append(similar_word)


cluster_group_withname = []
for c in range(0, numOfCluster):
    cluster_group_withname.append([])
    cluster_group_withname[c].append(most_similar_words[c])
    cluster_group_withname[c].append(cluster_to_words[c])
    print(most_similar_words[c])
    print(cluster_to_words[c])
    print("\n")
  
# save the cluster group with name  
with open('data/cluster_group_withname.txt', mode='wt', encoding='utf-8') as myfile:
    for item in cluster_name:
        for part in item:
            myfile.write("%s\n" % part)

# save only the names
with open('data/cluster_name.txt', mode='wt', encoding='utf-8') as myfile:
    myfile.write('\n'.join(most_similar_words))
    

