from flask import Flask, request, render_template, redirect, url_for
import flask
import couchdb
import json
import urllib.request
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
            if not self.db[doc]['alcohols_score'] == 0 and not self.db[doc]['fastfood_score'] == 0 and not self.db[doc]['smoking_score'] == 0:
                list.append(self.db[doc])
        return self.db

    """
    add a data entry to a database
    """
    def writeDoc2DB(self, data):
        self.db.save(data)


    def getHighRelevanceView(self):
        contents = urllib.request.urlopen("http://172.26.37.207:5984/result/_design/filter/_view/new-view?skip=0&reduce=false").read().decode()
        data = json.loads(contents)
        return data


    def loadData2Regions(self,data):
        with open('aus_regions.json') as f:
            regions = json.load(f)
        for r in regions['features']:
            value = self.getPlaceValue(data, r['properties']['Name'])
            r['num'] = value
        return regions

    # get the related value of the place
    def getPlaceValue(self, regions, regionName):
        if regions is None:
            return None
        for i in regions['rows']:
            if i['key'] == regionName:
                return i['value']
        return None


@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/mapPage')
def goToMap():
    return render_template('map.html')

@app.route('/regionMap')
def goToRegionMap():
    return render_template('regionsMap.html')


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



@app.route('/regionCount/<string:data_name>', methods=["GET"])
def smokeRegionCount(data_name):
    print(data_name)
    contents = {}
    if data_name == "Smoking":
        contents = urllib.request.urlopen("http://172.26.37.207:5984/result/_design/filter/_view/smoking?reduce=true&group_level=1").read().decode()
    elif data_name == "Fastfood":
        contents = urllib.request.urlopen("http://172.26.37.207:5984/result/_design/filter/_view/fastfood?reduce=true&group_level=1").read().decode()
    elif data_name == "Alcohols":
        contents = urllib.request.urlopen("http://172.26.37.207:5984/result/_design/filter/_view/alcohols?reduce=true&group_level=1").read().decode()
    data = json.loads(contents)
    db = Db("result")
    result = db.loadData2Regions(data)
    res = flask.make_response(flask.jsonify(result))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
