from flask import Flask, request, render_template, redirect, url_for
import flask
import couchdb
import json
import urllib.request
from shapely.geometry import shape, Point
app = Flask(__name__)
class Db:

    """
    Initial the couchDB with the given name
    """
    def __init__(self, dbname):
        user = "admin"
        password = "admin"
        self.couchserver = couchdb.Server("http://%s:%s@172.26.38.8:5984/" % (user, password))
        self.selectDb(dbname)
    """
    Select db by a given name
    """
    def selectDb(self, dbname):
        if dbname in self.couchserver:
            self.db = self.couchserver[dbname]
        else:
            self.db = self.couchserver.create(dbname)
    """
    Get all docs from db
    """
    def getAllDoc(self):
        list = []
        for doc in self.db:
            if not self.db[doc]['alcohols_score'] == 0 or \
                    not self.db[doc]['fastfood_score'] == 0 or \
                    not self.db[doc]['smoking_score'] == 0:
                list.append(self.db[doc])
        return self.db

    """
    add a data entry to a database
    """
    def writeDoc2DB(self, data):
        self.db.save(data)

    """
    get the topic-related tweets set
    """
    def getHighRelevanceView(self):
        mapData = "http://172.26.38.8:5984/results/_design/filter/_view/mapData?skip=0&reduce=false"
        contents = urllib.request.urlopen(mapData).read().decode()
        data = json.loads(contents)
        return data


    """
    map the data into the framework of the map
    """
    def loadData2Regions(self, data, analytics_data, key):
        with open('aus_regions.json') as f:
            regions = json.load(f)
        for r in regions['features']:
            res = self.getPlaceValue(data, analytics_data, r['properties']['Name'], key)
            if not res is None:
                value1, value2, value3 = res
                if value1 == 0 or value1 == None:
                    r['aurin_num'] = "no data in this area"
                else:
                    r['aurin_num'] = value1
                r['pos_num'] = value2
                r['neg_num'] = value3
            else:
                r['aurin_num'] = "no data in this area"
                r['pos_num'] = 0
                r['neg_num'] = 0
        return regions

    # get the related value of the place
    def getPlaceValue(self, regions, analytics_data, regionName,key):
        if regions is None:
            return None
        analytics_data = self.parse2Dic(analytics_data)
        for i in regions['features']:
            if i['properties']['lga_name'] == regionName:
                if regionName in analytics_data:
                    return i['properties'][key], analytics_data[regionName]['positive_portion'], analytics_data[regionName]['nagative_portion']
                else:
                    return i['properties'][key], 0, 0
        return None

    # parse the map reduce data into dict data structure
    def parse2Dic(self, data):
        data = json.loads(data)
        dic = {}
        for i in data['rows']:
            dic[i['key']] = i['value']
        return dic

    """
    get the city data for a particular city
    """
    def getCityTweetData(self, city, stat, aurin, key):
        result = []
        result1 = []
        with open("regionToCity.json") as f:
            dict = json.load(f)
        with open(aurin) as f:
            aurinData = json.load(f)

        for i in stat["rows"]:
            if i['key'] in dict:
                if dict[i['key']] == city:
                    for j in aurinData['features']:
                        aurinRegionName = j['properties']['lga_name']
                        if aurinRegionName == i['key'] and not j['properties'][key] == None:
                            result1.append([aurinRegionName, j['properties'][key]])
                            regionName = i['key']
                            value1 = i['value']['positive_portion']
                            value2 = i['value']['nagative_portion']
                            result.append([regionName, value1, value2 ])
        return result[:10], result1[:10]

    """
    Get the count for negative tweets and positive tweets for each city
    """
    def getCitySentCount(self, city, stat):
        result = []
        with open("regionToCity.json") as f:
            dict = json.load(f)
        data = json.loads(stat)
        pos = 0
        neg = 0
        for i in data["rows"]:
            if i['key'] in dict:
                if dict[i['key']] == city:

                    regionName = i['key']
                    value1 = i['value']['pos_count']
                    value2 = i['value']['neg_count']
                    pos = pos + value1
                    neg = neg + value2
                    result.append([regionName, value1, value2])
        return result

    # convert the region name into city name
    def getCoordinateRegion(self, region_file, city_file):
        data = {}
        with open(region_file) as f:
            regions = json.load(f)
        with open(city_file) as c:
            city_file = json.load(c)
        for r in regions['features']:
            c = r['geometry']['coordinates'][0][0][0]
            regionName = r['properties']['Name']
            for i in city_file['features']:
                city = i['properties']['CITY']
                s = shape(i['geometry'])
                point = Point(c[0], c[1])
                if s.contains(point):
                    data[regionName] = city
                    break
        return json.dumps(data)



smoking_url = "http://172.26.38.8:5984/results/_design/filter/_view/smoking?reduce=true&group_level=1&skip=0"
fastfood_url = "http://172.26.38.8:5984/results/_design/filter/_view/fastfood?reduce=true&group_level=1&skip=0"
alcohol_url = "http://172.26.38.8:5984/results/_design/filter/_view/alcohol?reduce=true&group_level=1&skip=0"
general_url = "http://172.26.38.8:5984/results/_design/filter/_view/counts?reduce=true&group_level=1&skip=0"
sentiment_url = "http://172.26.38.8:5984/results/_design/filter/_view/sentiment_count?reduce=true&group_level=1&skip=0&"

@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/mapPage')
def goToMap():
    return render_template('map.html')

@app.route('/regionMap')
def goToRegionMap():
    return render_template('regionsMap.html')

@app.route('/charts')
def goToChartPage():
    return render_template('charts.html')

@app.route('/data')
def getData():
    d = Db('results')
    result = d.getHighRelevanceView()
    res = flask.make_response(flask.jsonify(result))
    resp = formGetHeaders(res)
    return resp

@app.route('/pieChart')
def getPieChartData():
    piechart_data = urllib.request.urlopen(general_url).read().decode()
    p_data = json.loads(piechart_data)
    result = []
    for i in p_data['rows']:
        result.append([i['key'], i['value']])
    res = flask.make_response(flask.jsonify(result))
    resp = formGetHeaders(res)
    return resp


@app.route('/citySentData/<string:city>')
def getCitySentData(city):
    citySentData = urllib.request.urlopen(sentiment_url).read().decode()
    db = Db("results")
    result = db.getCitySentCount(city, citySentData)
    res = flask.make_response(flask.jsonify(result))
    resp = formGetHeaders(res)
    return resp


@app.route('/db/<string:db_name>', methods=["GET"])
def getAllFromDB(db_name):
    db = Db(db_name)
    data = {"reply": db.getAllDoc()}
    res = flask.make_response(flask.jsonify(data))
    resp = formGetHeaders(res)
    return resp


@app.route('/tweet_data/<string:city>/<string:data_name>/', methods=["GET"])
def getTweetsData(city, data_name):
    db = Db("tweets")
    if data_name == "Smoking":
        smoking_data = urllib.request.urlopen(smoking_url).read().decode()
        result = db.getCityTweetData(city, json.loads(smoking_data),"lung_cancer.json", 'lung_canc_2006_2010_num')
    elif data_name == "Fastfood":
        fastfood = urllib.request.urlopen(fastfood_url).read().decode()
        result = db.getCityTweetData(city, json.loads(fastfood), "overweight.json", 'est_ppl_18yrs_plus_obese_2014_15_num')
    elif data_name == "Alcohols":
        alcohol = urllib.request.urlopen(alcohol_url).read().decode()
        result = db.getCityTweetData(city, json.loads(alcohol), "high_blood_pressure.json",'est_ppl_18yrs_plus_hi_blood_pressure_2014_15_num')

    res = flask.make_response(flask.jsonify(result))
    resp = formGetHeaders(res)
    return resp

"""
Get the count of each scenario for each region
"""
@app.route('/regionCount/<string:data_name>', methods=["GET"])
def smokeRegionCount(data_name):
    db = Db("result")
    result = ""
    if data_name == "Smoking":
        with open("lung_cancer.json") as f:
            jsonData = json.load(f)
        smoking_data = urllib.request.urlopen(smoking_url).read().decode()
        result = db.loadData2Regions(jsonData, smoking_data,'lung_canc_2006_2010_num')
    elif data_name == "Fastfood":
        with open("overweight.json") as f:
            jsonData = json.load(f)
        fast_food = urllib.request.urlopen(fastfood_url).read().decode()
        result = db.loadData2Regions(jsonData, fast_food,  'est_ppl_18yrs_plus_obese_2014_15_num')
    elif data_name == "Alcohols":
        with open("high_blood_pressure.json") as f:
            jsonData = json.load(f)
        alcohol = urllib.request.urlopen(alcohol_url).read().decode()
        result = db.loadData2Regions(jsonData, alcohol ,'est_ppl_18yrs_plus_hi_blood_pressure_2014_15_num')

    res = flask.make_response(flask.jsonify(result))
    resp = formGetHeaders(res)
    return resp

"""
add a get header to the respoonse
"""
def formGetHeaders(res):
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8080)
