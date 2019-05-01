# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 23:02:56 2019
"""

from ahocorapy.keywordtree import KeywordTree
import sys

class Scorer:
    
    def __init__(self, analysor, dict_path):
        self.analysor = analysor
        
        self.searcher, self.words, self.weight = self.searcher(dict_path)
    '''
        Get the related keywords and corresponding weights
        searchResult: the result returned by kwtree2.search_all
    '''
    def KeywordWeight(self,searchResult, words, weights):
        keyword = []
        keyword_weight = []
        for result in searchResult:
            keyword.append(result[0])
        for k in keyword:
            for i in range(len(words)):
                if words[i] == k:
                    keyword_weight.append(weights[i])
                    break
        return keyword, keyword_weight
    
    '''
        Get the score of the word in terms of specific topics
    '''
    def scoring(self,keyword, weight, real_sentiment, intended_sentiment, sentilevel):
        score = 0
        for i in range(len(weight)):
            score += float(weight[i])
        if real_sentiment == intended_sentiment:
            discount = sentilevel
        else:
            discount = -sentilevel
        score = score * discount
        return score
    
    '''
        Get the related words in the dictionary and put them into KeywordTree
    '''
    def searcher(self,filepath):
        kwtree_word = []
        kwtree_weight = []
        f = open(filepath)
        for line in f:
            word, weight = line.split(' ')
            word = word.replace('_', ' ')
            kwtree_word.append(word)
            weight = weight.split('\n')[0]
            kwtree_weight.append(weight)
        f.close()
        kwtree = KeywordTree(case_insensitive=True)
        for word in kwtree_word:
            kwtree.add(word)
        kwtree.finalize()
        return kwtree, kwtree_word, kwtree_weight
    
    '''
        The main entry
    '''
    def get_score(self, tweet,intended_sentiment):
        search_result = self.searcher.search_all(tweet)
        keyword, keyword_weight = self.KeywordWeight(search_result, self.words, self.weight)
        prediction = self.analysor.prediction(tweet)
        real_senti = prediction[0]
        sentilevel = prediction[1]
        score = self.scoring(keyword, keyword_weight, intended_sentiment, real_senti, sentilevel)
        return score