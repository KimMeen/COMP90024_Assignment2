# -*- coding: utf-8 -*-
"""
Created on Sat May 11 11:48:26 2019

@author: 39932
"""

import couchdb
import json

db_server = couchdb.Server("http://admin:admin@127.0.0.1:5984/")
db_name = "results"
alcohol_name = "alcohols"
smoking_name = "smoking"
fastfood_name = "fast_food"

if alcohol_name not in db_server:
    db_server.create(alcohol_name)
if smoking_name not in db_server:
    db_server.create(smoking_name)
if fastfood_name not in db_server:
    db_server.create(fastfood_name)

alcohol_db = db_server[alcohol_name]
smoking_db = db_server[smoking_name]
fastfood_db = db_server[fastfood_name]

if db_name in db_server:
    db = db_server[db_name]
    alcohol = []
    smoking = []
    fastfood = []
    alcohol_buffer = 0  
    smoking_buffer = 0
    fastfood_buffer = 0
    index = 0
    for ele in db:
        index += 1
        print (index)
        document = db[ele]
        if not ("alcohols_score" in document and "fastfood_score" in document and "smoking_score" in document):
            continue
        if (document["alcohols_score"] == 0 and document["fastfood_score"] == 0 and document["smoking_score"] == 0):
            continue
        id = document["_id"]
        text = document["text"]
        coordinates = document["coordinates"]
        region = document["region"]
        label = "Negative" if document["label"]==0 else "Positive"
        alcohols_sc = document["alcohols_score"]
        fastfood_sc = document["fastfood_score"]
        smoking_sc = document["smoking_score"]
        if document["alcohols_score"] > 0:
            alcohol_buffer += 1
            data = {"_id":id,
                    "text":text,
                    "coordinates":coordinates,
                    "label":label,
                    "alcohols_score":alcohols_sc}
            alcohol.append(data)
            if alcohol_buffer == 1000:
                alcohol_db.update(alcohol)
                alcohol = []
                alcohol_buffer = 0
        if document["fastfood_score"] > 0:
            fastfood_buffer += 1
            data = {"_id":id,
                    "text":text,
                    "coordinates":coordinates,
                    "label":label,
                    "fastfood_score":fastfood_sc}
            fastfood.append(data)
            if fastfood_buffer == 1000:
                fastfood_db.update(fastfood)
                fastfood = []
                fastfood_buffer = 0
        if document["smoking_score"] > 0:
            smoking_buffer += 1
            data = {"_id":id,
                    "text":text,
                    "coordinates":coordinates,
                    "label":label,
                    "smoking_score":smoking_sc}
            smoking.append(data)
            if smoking_buffer == 1000:
                smoking_db.update(smoking)
                smoking = []
                smoking_buffer = 0
    
    if len(alcohol) != 0:
        alcohol_db.update(alcohol)
    if len(fastfood) != 0:
        fastfood_db.update(fastfood)
    if len(smoking) != 0:
        smoking_db.update(smoking)
    print("done")
                
            