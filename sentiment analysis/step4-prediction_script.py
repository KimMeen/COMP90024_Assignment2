# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 21:49:03 2019

@author: Ming Jin
"""

import numpy as np
import sys
import pickle
from keras.preprocessing.sequence import pad_sequences
from keras.utils import CustomObjectScope
from keras.models import load_model
from keras.initializers import glorot_uniform

def top_n_words(pkl_file_name, N, shift=0):
    with open(pkl_file_name, 'rb') as pkl_file:
        freq_dist = pickle.load(pkl_file)
    most_common = freq_dist.most_common(N)
    words = {p[0]: i + shift for i, p in enumerate(most_common)}
    return words

def get_feature_vector(tweet):
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

if __name__ == '__main__':
    
    # raw sentence
    raw_sentence = input("\nInput a sentence to predict => ")
    print('\n')
    # load the model
    with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
        model = load_model('D:\\COMP90024_Assignment2\\sentiment analysis\\sentiment_lstm.h5')
    
    # pre-defined params
    unigrams_file = 'D:\\COMP90024_Assignment2\\sentiment analysis\\training_data\\large\\sentiment140-freqdist.pkl'
    label = ['NEGATIVE', 'POSITIVE']
    max_length = 40
    vocab_size = 90000
    vocab = top_n_words(unigrams_file, vocab_size, shift=1)
    
    # get the prediction
    test_tweet_vector = get_feature_vector(raw_sentence)
    test_tweet_vector = np.reshape(test_tweet_vector, (1, len(test_tweet_vector)))
    test_tweet_vector = pad_sequences(test_tweet_vector, maxlen = max_length, padding = 'post')
    predictions = model.predict(test_tweet_vector, batch_size=128, verbose=1)
    results = label[np.round(predictions[:, 0]).astype(int)[0]]
    print('\n\n  ==> A.I. Prediction: This sentence seems a', results, 'one.')