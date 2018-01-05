import wikipediaapi
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


# Give a word for each cluster
most_similar_words=[]
for i in range(0, numOfCluster):
    #print(i)
    model_word_vector = np.array(kmeans_model.cluster_centers_[i], dtype='f')
    similar_word = w2v_model.most_similar( [ model_word_vector ], [], topn=1)[0][0]  
    most_similar_words.append(similar_word)

for c in range(0, numOfCluster):
    print(most_similar_words[c])
    print(cluster_to_words[c])
    print("\n")











