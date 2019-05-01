#!/usr/bin/env python
# coding: utf-8

import logging
import couchdb
import json
import sys
sys.path.append('./sentiment analysis/release')
import sentiment_prediction as senti
sys.path.append('./topic analysis')
import scorer
sys.path.append('../util')
import text_util
# sys.path.append('../util')
# import MapRegion

'''
    Get the source db(the db created by harverster)
    and the destination db (store the result)
'''
def get_source_db():
    config = None
    db_server = None
    source_db = None
    with open("db_config.json") as cf:
        config = json.load(cf)
        try:
            db_server = couchdb.Server(config["Servers"][0])
            source_db_name = config["DB"][0]
            if source_db_name not in db_server:
                logging.error("Database %s does not exist, something went wrong." %(source_db_name))
                return
            source_db = db_server[source_db_name]
        except Exception as e:
            logging.error("error happened: %s" %e)
            sys.exit(2)
    return source_db

def get_dest_db():
    config = None
    db_server = None
    dest_db = None
    with open("db_config.json") as cf:
        config = json.load(cf)
        try:
            db_server = couchdb.Server(config["Servers"][0])
            dest_db_name = config["DB"][1]
            if dest_db_name in db_server:
                dest_db = db_server[dest_db_name]
        except Exception as e:
            logging.error("error happened: %s" %e)
            sys.exit(2)
    return dest_db

def create_dest_db():
    config = None
    db_server = None
    dest_db = None
    with open("db_config.json") as cf:
        config = json.load(cf)
        try:
            db_server = couchdb.Server(config["Servers"][0])
            dest_db_name = config["DB"][1]
            if dest_db_name in db_server:
                logging.info("db has existed, create a new one")
                db_server.delete(dest_db_name)
                dest_db = db_server.create(dest_db_name)
            else:
                dest_db = db_server.create(dest_db_name)
        except Exception as e:
            logging.error("error happened: %s" %e)
            sys.exit(2)
    return dest_db

'''
    This is the excution part,
    the analysis result will be returned
'''
def analyze(document,senti_analyzer,alcohols_scorer,fastfood_scorer,smoking_scorer):
    created_at = document["created_at"]
    raw_text = document["text"]
    location = document["location"]
    coordinates = document["coordinates"]
    label, proba = senti_analyzer.prediction(raw_text)
    new_text = text_util.preprocess_tweet(raw_text)
    # 0:NEGATIVE 1:POSITIVE
    label_flag = 0 if label=="NEGATIVE" else 1
    ##########add Region here###################
    alcohols_sc = alcohols_scorer.get_score_v2(new_text)
    fastfood_sc = fastfood_scorer.get_score_v2(new_text)
    smoking_sc = smoking_scorer.get_score_v2(new_text)
    return {"created_at":created_at,"text":new_text,"label":label_flag,"probability":proba,
                       "alcohols_score":alcohols_sc,"fastfood_score":fastfood_sc,"smoking_score":smoking_sc}



from mpi4py import MPI

comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()

modelpath = './sentiment analysis/model/sentiment_lstm.h5'
pklpath = './sentiment analysis/model/sentiment140-freqdist.pkl'
senti_analyzer = senti.sentianalyser(modelpath, pklpath, stemmer = False)
if comm_rank == 0:
    source_db = get_source_db()
    dest_db = create_dest_db()
else:
    source_db = get_source_db()
    dest_db = None
    while dest_db == None:
        dest_db = get_dest_db()
alcohols_dict = "./topic analysis/dictionary/alcohols.txt"
fastfood_dict = "./topic analysis/dictionary/fastfood.txt"
smoking_dict = "./topic analysis/dictionary/smoking.txt"
alcohols_scorer = scorer.Scorer(senti_analyzer, alcohols_dict)
fastfood_scorer = scorer.Scorer(senti_analyzer, fastfood_dict)
smoking_scorer = scorer.Scorer(senti_analyzer, alcohols_dict)
index = 0
buffer = 0
result = []
for ele in source_db:
    index += 1
    print(index)
    if index % comm_size == comm_rank: 
        buffer += 1
        document = source_db[ele]
        result.append(analyze(document,senti_analyzer,alcohols_scorer,fastfood_scorer,smoking_scorer))
        if buffer == 100:
            dest_db.update(result)
            buffer = 0
            result = []
if buffer != 0 and len(result) != 0:
    dest_db.update(result)
print("rank %s Analyzing successfully!" %comm_rank)





