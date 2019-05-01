# -*- coding: utf-8 -*-
"""
Created on Wed May  1 13:03:03 2019

@author: 39932
"""

import re
from nltk.stem.porter import PorterStemmer

def is_valid_word(word):
        return (re.search(r'^[a-zA-Z][a-z0-9A-Z\._]*$', word) is not None)
    
    
def preprocess_word(word):
    word = word.strip('\'"?!,.():;')
    word = re.sub(r'(.)\1+', r'\1\1', word)
    word = re.sub(r'(-|\')', '', word)
    return word
    
    
def handle_emojis(tweet):
    tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', ' EMO_POS ', tweet)
    tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' EMO_POS ', tweet)
    tweet = re.sub(r'(<3|:\*)', ' EMO_POS ', tweet)
    tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', ' EMO_POS ', tweet)
    tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' EMO_NEG ', tweet)
    tweet = re.sub(r'(:,\(|:\'\(|:"\()', ' EMO_NEG ', tweet)
    return tweet
    
    
def preprocess_tweet(tweet,use_stemmer=False):
    processed_tweet = []
    tweet = tweet.lower()
    tweet = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', '', tweet)
    tweet = re.sub(r'@[\S]+', '', tweet)
    tweet = re.sub(r'#(\S+)', r' \1 ', tweet)
    tweet = re.sub(r'\brt\b', '', tweet)
    tweet = re.sub(r'\.{2,}', ' ', tweet)
    tweet = tweet.strip(' "\'')
    tweet = handle_emojis(tweet)
    tweet = re.sub(r'\s+', ' ', tweet)
    words = tweet.split()
    
    for word in words:
        word = preprocess_word(word)
        if is_valid_word(word):
            if use_stemmer:
                porter_stemmer = PorterStemmer()
                word = str(porter_stemmer.stem(word))
            processed_tweet.append(word)
    return ' '.join(processed_tweet)

