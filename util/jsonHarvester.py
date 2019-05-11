import sys
import os
import couchdb
import MapRegion
import text_util
import formatTime
import json

def process_tweet(tweet_json, db, region_file):
    if (tweet_json["doc"]["coordinates"] is not None):
        submitted_json = {}
        submitted_json['_id'] = tweet_json["id"]
        submitted_json['created_at'] = formatTime.to_datetime(tweet_json["doc"]["created_at"])
        submitted_json['text'] = text_util.preprocess_tweet(tweet_json["doc"]["text"])
        submitted_json['coordinates'] = [tweet_json["doc"]["coordinates"]["coordinates"][1],
                                        tweet_json["doc"]["coordinates"]["coordinates"][0]]
        
        submitted_json['region'] = MapRegion.getCoordinateRegion(submitted_json['coordinates'], region_file)
        if (submitted_json['text'] != ""):
            try:
                db.save(submitted_json)
            except:
                pass

def parseJson(tweet_row):
    try:
        tweet_json = json.loads(tweet_row[:-3])
        return tweet_json
    except:
        try:
            tweet_json = json.loads(tweet_row[:-2])
            return tweet_json
        except:
            return None


def harvest_json_couchdb(file_path, couchdb_server, db_name, region_file):
    with open(file_path,"r") as f:
        db = couchdb_server[db_name]
        for index, line in enumerate(f):
            tweet_json = parseJson(line)
            if tweet_json is not None:
                process_tweet(tweet_json, db, region_file)

if __name__ == "__main__":
    couch = couchdb.Server()
    couch = couchdb.Server('http://admin:admin@master-node:5984/')
    harvest_json_couchdb("./teacher_db/twitter_sydney.json", couch, "tweets")
