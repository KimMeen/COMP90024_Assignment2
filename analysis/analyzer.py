#!/usr/bin/env python
# coding: utf-8

import couchdb
import json
import sys
sys.path.append('./sentiment analysis/release')
import sentiment_prediction as senti
sys.path.append('./topic analysis')
import scorer


'''
    Get the source db(the db created by harverster).
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
                print("Database %s does not exist, something went wrong." %(source_db_name))
                return
            source_db = db_server[source_db_name]
        except Exception as e:
            print("error happened: %s" %e)
            sys.exit(2)
    return source_db

'''
    Get the destination DB which stores the 
    analysis result.
'''

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
            print("error happened: %s" %e)
            sys.exit(2)
    return dest_db

'''
    Master node is responsible to create the destination DB
    if it didn't exist before.
'''
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
                print("db has existed, create a new one")
                db_server.delete(dest_db_name)
                dest_db = db_server.create(dest_db_name)
            else:
                dest_db = db_server.create(dest_db_name)
        except Exception as e:
            print("error happened: %s" %e)
            sys.exit(2)
    return dest_db

'''
    This is the excution part,
    the analysis result will be returned.
    document:meta data of couchDB which contains information about one tweet 
    in the form of JSON.
'''
def analyze(document,senti_analyzer,alcohols_scorer,fastfood_scorer,smoking_scorer):
    id = document["_id"]
    created_at = document["created_at"]
    text = document["text"]
    coordinates = document["coordinates"]
    label, proba = senti_analyzer.prediction(text)
    # 0:NEGATIVE 1:POSITIVE
    label_flag = 0 if label=="NEGATIVE" else 1
    region = document["region"]
    #calculate the score about these three topics
    alcohols_sc = alcohols_scorer.get_score_v2(text)
    fastfood_sc = fastfood_scorer.get_score_v2(text)
    smoking_sc = smoking_scorer.get_score_v2(text)
    return {"_id":id,"created_at":created_at,"text":text,"label":label_flag,"region":region,"probability":proba,"coordinates":coordinates,
                       "alcohols_score":alcohols_sc,"fastfood_score":fastfood_sc,"smoking_score":smoking_sc}

'''
    MPI implementation
'''
from mpi4py import MPI
import time

comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()
start_time = time.time()
modelpath = './sentiment analysis/model/sentiment_lstm.h5'
pklpath = './sentiment analysis/model/sentiment140-freqdist.pkl'
senti_analyzer = senti.sentianalyser(modelpath, pklpath, stemmer = False)
# Master node needs to create the destination DB if it doesn't exist 
if comm_rank == 0:
    source_db = get_source_db()
    dest_db = get_dest_db()
    if dest_db is None:
        dest_db = create_dest_db()
else:
    source_db = get_source_db()
    dest_db = None
    # Get the destination DB in loop in case of concurrecy proble,
    # that is, slave nodes try to acquire the dest DB before master node creates it.
    while dest_db == None:
        dest_db = get_dest_db()
alcohols_dict = "./topic analysis/dictionary/alcohols.txt"
fastfood_dict = "./topic analysis/dictionary/fastfood.txt"
smoking_dict = "./topic analysis/dictionary/smoking.txt"
# create Scorer objects for each topic 
# so that the resource only needs to be loaded once. 
alcohols_scorer = scorer.Scorer(senti_analyzer, alcohols_dict)
fastfood_scorer = scorer.Scorer(senti_analyzer, fastfood_dict)
smoking_scorer = scorer.Scorer(senti_analyzer, smoking_dict)
# index records the number of tweets 
index = 0
# records the number of results in the buffer
buffer = 0
# A temporary list to store results.
# if the buffer is full, data in result will be written into dest DB,
# and buffer and result will be reset.
result = []
for ele in source_db:
    index += 1
    print(index)
    # each node only handles the tweets they are responsible for.
    if index % comm_size == comm_rank:
        if ele in dest_db:
            continue
        buffer += 1
        document = source_db[ele]
        result.append(analyze(document,senti_analyzer,alcohols_scorer,fastfood_scorer,smoking_scorer))
        if buffer == 100:
            dest_db.update(result)
            buffer = 0
            result = []
# If the buffer is not empty, store the rest of the results into dest DB.
if buffer != 0 and len(result) != 0:
    dest_db.update(result)
end_time = time.time()
print("rank %s Analyzing successfully! time consumed: %s" %(comm_rank,(end_time-start_time)))
