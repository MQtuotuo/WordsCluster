import wikipedia
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

wiki_wiki = wikipediaapi.Wikipedia('en')

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


# get the cluster name
cluster_words=[]
with open('data/cluster_name.txt', mode='r', encoding='utf-8') as myfile:   
    for line in myfile:
        cluster_words.append(line)
cluster_words = [x.strip() for x in cluster_words] 


def getTopSection(sections, clusterWord):
    section_title=[]
    for s in sections:
        section_title.append([s.title, phrase_similarity(clusterWord, s.title, w2v_model)])
    simi_list = [i[1] for i in section_title]
    index = simi_list.index(max(simi_list))
    selected_section = sections[index]
    text = sections[index].text
    return selected_section, text

def getSummary(answer, keyword, relation):
    summary = []
    
    if relation==None:
        word_vector=phrase_vector(answer, w2v_model)
        
    else:
        word_vector=phrase_vector(relation, w2v_model)
        
    label = kmeans_model.predict(word_vector)[0]
    clusterWord = cluster_words[label]
    #print(clusterWord)
    
    
    # get the top page by using answer entity
    if len(wikipedia.search(answer))==0:
        summary=None
        return summary
    else:
        pagename=wikipedia.search(answer)[0]
        page = wiki_wiki.page(pagename)
    
        # get the sections with more information related to the cluster word
        selected_section, text_section =getTopSection(page.sections, clusterWord)
    
    #print(selected_section.title, "section has", len(selected_section.sections), "subsections")
    #print('='*50)
        if len(selected_section.sections)<=1:
            summary.append(page.summary)
            summary.append(text_section)
        else:
            selected_subsection, text_subsection= getTopSection(selected_section.sections, keyword)
            summary.append(page.summary)
            summary.append(text_subsection)
        return summary[0]+summary[1]











