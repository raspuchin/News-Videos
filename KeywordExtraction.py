#!/usr/bin/env python
# coding: utf-8
# @Author : Sachin Pothukuchi
# @Github: raspuchin


from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from scipy.sparse import coo_matrix
import pickle
import os
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import re
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer

nltk.download('wordnet') 
from nltk.stem.wordnet import WordNetLemmatizer


cv = None
tfidf_transformer = None
feature_names = None
stop_words = None


def load():
    global stop_words
    global cv
    global tfidf_transformer
    global feature_names
    stop_words = set(stopwords.words("english"))
    new_words = ["using", "show", "result", "large", "also", "iv", "one", "two", "new", "previously", "shown"]
    stop_words = stop_words.union(new_words)
    cv, tfidf_transformer, feature_names = pickle.load(open('vector.pickel','rb'))

def preprocess(articles):
    corp = []
    for text in articles:
        #Remove punctuations
        text = re.sub('[^a-zA-Z]', ' ', text)

        #Convert hashtags from camel case to normal text
        text = ' '.join(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', text))
        
        #Convert to lowercase
        text = text.lower()

        #remove tags
        text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)

        # remove special characters and digits
        text=re.sub("(\\d|\\W)+"," ",text)

        ##Convert to list from string
        text = text.split()

        ##Stemming
        ps=PorterStemmer()
        #Lemmatisation
        lem = WordNetLemmatizer()
        text = [lem.lemmatize(word) for word in text if not word in stop_words] 
        text = ' '.join(text)
        corp.append(text)
    return corp

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
 
def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]
 
    score_vals = []
    feature_vals = []
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
 
    #create a tuples of feature,score
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results

def getKeywordList(article):
    corpus = preprocess([article])
    tf_idf_vector=tfidf_transformer.transform(cv.transform(corpus))
    sorted_items=sort_coo(tf_idf_vector.tocoo())
    keywords=extract_topn_from_vector(feature_names,sorted_items)
    keywords = sorted(keywords, key=len)
    keywords = [j for i,j in enumerate(keywords) if all(j not in k for k in keywords[i + 1:]) ]
    return keywords

