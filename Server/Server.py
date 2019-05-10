from flask import Flask, request, render_template, redirect, url_for
import flask
import couchdb
import json
import urllib.request
import time
from shapely.geometry import shape, Point
app = Flask(__name__)
class Db:

    """
    Initial the couchDB with the given name
    """
    def __init__(self, dbname):
        user = "admin"
        password = "admin"
        self.couchserver = couchdb.Server("http://%s:%s@172.26.37.207:5984/" % (user, password))
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

    def getHighRelevanceView(self):
        contents = urllib.request.urlopen("http://172.26.37.207:5984/results/_design/filter/_view/new-view?skip=0").read().decode()
        data = json.loads(contents)
        return data


    # map the data into the framework of the map
    def loadData2Regions(self,data, analytics_data, key):
        with open('aus_regions.json') as f:
            regions = json.load(f)
        for r in regions['features']:
            res = self.getPlaceValue(data, analytics_data, r['properties']['Name'], key)
            if not res is None:
                value1, value2 = res
                r['aurin_num'] = value1
                r['analytics_num'] = value2
            else:
                r['aurin_num'] = None
                r['analytics_num'] = 0
        return regions

    # get the related value of the place
    def getPlaceValue(self, regions, analytics_data, regionName,key):
        if regions is None:
            return None
        analytics_data = self.parse2Dic(analytics_data)
        for i in regions['features']:
            if i['properties']['lga_name'] == regionName:
                if regionName in analytics_data:
                    return i['properties'][key], analytics_data[regionName]['portion']
                else:
                    return i['properties'][key], 0
        return None

    # parse the map reduce data into dict data structure
    def parse2Dic(self, data):
        data = json.loads(data)
        dic = {}
        for i in data['rows']:
            dic[i['key']] = i['value']
        return dic

    # get aurin data with the mapped city name
    def getCityAurinData(self, city, stat):
        result = []
        with open("regionToCity.json") as f:
            dict = json.load(f)
        with open(stat) as f:
            data = json.load(f)
        for i in data['features']:
            regionName = i['properties']['lga_name']
            if regionName in dict and not i['properties']['lung_canc_2006_2010_num'] == None:
                if dict[regionName] == city:
                    x = i['properties']['lga_name']
                    value = i['properties']['lung_canc_2006_2010_num']
                    result.append([x,value])
        result.sort(key=lambda x: x[1], reverse=True )
        return result[:10]

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
                            value = i['value']['portion']
                            result.append([regionName, value])
        print(result1)
        return result[:10], result1[:10]


    def getCombineData(self, city, stat, key):
        result = []
        with open("regionToCity.json") as f:
            dict = json.load(f)
        with open(stat) as f:
            data = json.load(f)

        for i in stat["rows"]:
            if i['key'] in dict:
                if dict[i['key']] == city:
                    regionName = i['key']
                    value = i['value']
                    for i in data['features']:
                        if regionName == i['properties']['lga_name'] and not i[key] == None:
                            value2 = i['properties'][key]
                            result.append([regionName, value, value2])
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

smoking_url = "http://172.26.37.207:5984/results/_design/filter/_view/smoking?reduce=true&group_level=1&skip=0"
fastfood_url = "http://172.26.37.207:5984/results/_design/filter/_view/fastfood?reduce=true&group_level=1&skip=0"
alcohol_ulr = "http://172.26.37.207:5984/results/_design/filter/_view/alcohol?reduce=true&group_level=1&skip=0"
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
    d = Db('result')
    result = d.getHighRelevanceView()
    ans = flask.make_response(flask.jsonify(result))
    ans.headers['Access-Control-Allow-Origin'] = '*'
    ans.headers['Access-Control-Allow-Methods'] = 'GET'
    ans.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return ans

@app.route('/db/<string:db_name>', methods=["GET"])
def getAllFromDB(db_name):
    db = Db(db_name)
    data = {"reply": db.getAllDoc()}
    res = flask.make_response(flask.jsonify(data))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res


@app.route('/aurin/<string:city>/<string:type>', methods=["GET"])
def getAurinCityData(city, type):
    db = Db('tweets')
    res = flask.make_response(flask.jsonify(db.getCityAurinData(city, type)))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res

@app.route('/tweet_data/<string:city>/<string:data_name>/', methods=["GET"])
def getTweetsData(city, data_name):
    db = Db("tweets")
    print(city)
    if data_name == "Smoking":
        smoking_data = urllib.request.urlopen(smoking_url).read().decode()
        result = db.getCityTweetData(city, json.loads(smoking_data),"lung_cancer.json", 'lung_canc_2006_2010_num')
    elif data_name == "Fastfood":
        fastfood = urllib.request.urlopen(fastfood_url).read().decode()
        result = db.getCityTweetData(city, json.loads(fastfood), "overweight.json", 'est_ppl_18yrs_plus_obese_2014_15_num')
    elif data_name == "Alcohols":
        alcohol = urllib.request.urlopen(alcohol_ulr).read().decode()
        result = db.getCityTweetData(city, json.loads(alcohol), "high_blood_pressure.json",'est_ppl_18yrs_plus_hi_blood_pressure_2014_15_num')
    res = flask.make_response(flask.jsonify(result))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res


@app.route('/regionCount/<string:data_name>', methods=["GET"])
def smokeRegionCount(data_name):
    print(data_name)
    db = Db("result")
    result=""
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
        alcohol = urllib.request.urlopen(alcohol_ulr).read().decode()
        result = db.loadData2Regions(jsonData, alcohol ,'est_ppl_18yrs_plus_hi_blood_pressure_2014_15_num')

    res = flask.make_response(flask.jsonify(result))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
    # d = Db("tweets_city")
    # d.getCityAurinData("Adelaide", "lung_cancer.json")
