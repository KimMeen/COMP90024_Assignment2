# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 15:28:35 2019

@author: Ming Jin
"""

import numpy as np
import pickle
import re
from nltk.stem.porter import PorterStemmer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import CustomObjectScope
from keras.models import load_model
from keras.initializers import glorot_uniform


class sentianalysor:
    '''
    This analysor has been created to do the sentiment analysis
    
    These methods has been defined:
        |-- is_valid_word: To judge if the given word valid or not
        |-- preprocess_word: To process the given word
        |-- handle_emojis: To process the emojs in tweet
        |-- preprocess_tweet: To process the tweet by invoking the previous methods
        |-- top_n_words: To generate the frequency dictionary
        |-- get_feature_vector: To generate the feature vector based on dict
        |-- senti_level: To calcualte the sentimental level
        |-- prediction: To make the prediction on the given tweet
    '''
    
    def __init__(self, modelpath, freqdist, stemmer = False):
        self.freqdist = freqdist
        self.max_length = 40
        self.vocab_size = 90000
        self.use_stemmer = stemmer
        self.label = ['NEGATIVE', 'POSITIVE']


        with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
            self.model = load_model(modelpath)
    
    
    def is_valid_word(self, word):
        return (re.search(r'^[a-zA-Z][a-z0-9A-Z\._]*$', word) is not None)
    
    
    def preprocess_word(self, word):
        word = word.strip('\'"?!,.():;')
        word = re.sub(r'(.)\1+', r'\1\1', word)
        word = re.sub(r'(-|\')', '', word)
        return word
    
    
    def handle_emojis(self, tweet):
        tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', ' EMO_POS ', tweet)
        tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' EMO_POS ', tweet)
        tweet = re.sub(r'(<3|:\*)', ' EMO_POS ', tweet)
        tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', ' EMO_POS ', tweet)
        tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' EMO_NEG ', tweet)
        tweet = re.sub(r'(:,\(|:\'\(|:"\()', ' EMO_NEG ', tweet)
        return tweet
    
    
    def preprocess_tweet(self, tweet):
        processed_tweet = []
        tweet = tweet.lower()
        tweet = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', '', tweet)
        tweet = re.sub(r'@[\S]+', '', tweet)
        tweet = re.sub(r'#(\S+)', r' \1 ', tweet)
        tweet = re.sub(r'\brt\b', '', tweet)
        tweet = re.sub(r'\.{2,}', ' ', tweet)
        tweet = tweet.strip(' "\'')
        tweet = self.handle_emojis(tweet)
        tweet = re.sub(r'\s+', ' ', tweet)
        words = tweet.split()
    
        for word in words:
            word = self.preprocess_word(word)
            if self.is_valid_word(word):
                if self.use_stemmer:
                    porter_stemmer = PorterStemmer()
                    word = str(porter_stemmer.stem(word))
                processed_tweet.append(word)
        
        return ' '.join(processed_tweet)
    
    
    def top_n_words(self, freqdist, N, shift = 0):
        with open(freqdist, 'rb') as pkl_file:
            freq_dist = pickle.load(pkl_file)
        most_common = freq_dist.most_common(N)
        words = {p[0]: i + shift for i, p in enumerate(most_common)}
        return words
    
    
    def get_feature_vector(self, tweet, vocab):
        words = tweet.split()
        feature_vector = []
        for i in range(len(words) - 1):
            word = words[i]
            if vocab.get(word) is not None:
                feature_vector.append(vocab.get(word))
        if len(words) >= 1:
            if vocab.get(words[-1]) is not None:
                feature_vector.append(vocab.get(words[-1]))
        return feature_vector
    
    
    def senti_level(self, prediction):
        prob = prediction[-1][0]
        if prob > 0.5:
            level = float(prob / 1)
        else:
            level = float((1-prob) / 1)          
        return level
    
    
    def prediction(self, tweet):
        raw_tweet = tweet
        precessed_tweet = self.preprocess_tweet(raw_tweet)
        vocab = self.top_n_words(self.freqdist, self.vocab_size, shift=1)
        feature_vector =self.get_feature_vector(precessed_tweet, vocab)
        feature_vector = np.reshape(feature_vector, (1, len(feature_vector)))
        feature_vector = pad_sequences(feature_vector, maxlen = self.max_length, padding = 'post')
        predictions = self.model.predict(feature_vector)
        level = self.senti_level(predictions)
        result = self.label[np.round(predictions[:, 0]).astype(int)[0]]
        return result, level
        
        