# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 15:20:33 2019

@author: Ming Jin

This python script used to preprocess the raw tweet 
and transform them into the normalized format.
"""

import re
import sys
from nltk.stem.porter import PorterStemmer

def write_status(i, total):
    ''' 
    Writes status of a process to the console 
    '''
    sys.stdout.write('\r')
    sys.stdout.write('Processing %d/%d' % (i, total))
    sys.stdout.flush()

def preprocess_word(word):
    '''
    This method used to normalize a given word,
    e,g., The word 'gooood!' will be normalized
    to 'good'
    '''
    word = word.strip('\'"?!,.():;')
    word = re.sub(r'(.)\1+', r'\1\1', word)
    word = re.sub(r'(-|\')', '', word)
    return word

def is_valid_word(word):
    '''
    To judge if a given word is valild or not
    '''
    return (re.search(r'^[a-zA-Z][a-z0-9A-Z\._]*$', word) is not None)

def handle_emojis(tweet):
    '''
    Transform some emoji sambols, e.g., :( or :), to tags
    '''
    tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', ' EMO_POS ', tweet)
    tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' EMO_POS ', tweet)
    tweet = re.sub(r'(<3|:\*)', ' EMO_POS ', tweet)
    tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', ' EMO_POS ', tweet)
    tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' EMO_NEG ', tweet)
    tweet = re.sub(r'(:,\(|:\'\(|:"\()', ' EMO_NEG ', tweet)
    return tweet

def preprocess_tweet(tweet):
    '''
    This method invokes the above methods to
    process a given raw tweet
    '''
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
                word = str(porter_stemmer.stem(word))
            processed_tweet.append(word)

    return ' '.join(processed_tweet)

def preprocess_csv(csv_file_name, processed_file_name):
    '''
    The main entry of the precessing, which invokes
    preprocess_tweet method to batch process the recordings
    in the given csv file
    '''
    save_to_file = open(processed_file_name, 'w')

    with open(csv_file_name, 'r', encoding = 'mac_roman') as csv:
        lines = csv.readlines()
        total = len(lines)
        for i, line in enumerate(lines):
            label = line[:line.find(',')]
            label = filter(str.isdigit, label)
            label = int("".join(label))
            line = line[1 + line.find(','):]
            tweet_id = line[:line.find(',')]
            line = line[1 + line.find(','):]
            line = line[1 + line.find(','):]
            line = line[1 + line.find(','):]
            line = line[1 + line.find(','):]
            tweet = line
            processed_tweet = preprocess_tweet(tweet)
            save_to_file.write('%s,%d,%s\n' %
                                   (tweet_id, label, processed_tweet))
            write_status(i + 1, total)
    save_to_file.close()
    print('\nSaved processed tweets to: %s' % processed_file_name)
    return processed_file_name

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python preprocess.py <raw-tweets.csv>')
        exit()
    use_stemmer = False
    csv_file_name = sys.argv[1]
    processed_file_name = sys.argv[1][:-4] + '-processed.csv'
    if use_stemmer:
        porter_stemmer = PorterStemmer()
        processed_file_name = sys.argv[1][:-4] + '-processed-stemmed.csv'
    preprocess_csv(csv_file_name, processed_file_name)