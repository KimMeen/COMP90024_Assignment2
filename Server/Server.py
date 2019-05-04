from flask import Flask, request
import flask
import couchdb
import json
import urllib.request
import MapRegion
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
            list.append(self.db[doc])
        return self.db

    """
    add a data entry to a database
    """
    def writeDoc2DB(self, data):
        self.db.save(data)

    def loadWebData(self):
        with open('aus_regions.json') as f:
            regions = json.load(f)
        for r in regions['features']:
            value = self.getPlaceValue(regions, r['properties']['Name'])
            r['sentiment_score'] = value
        with open("../WebPage/regionsData.json", "w") as out:
            out.write("var statistic = " + json.dumps(regions))

    # get the related value of the place
    def getPlaceValue(self, regions, regionName):
        if regions is None:
            return None
        for i in regions['rows']:
            if i['key'] == regionName:
                return i['value']
        return None


@app.route('/')
def home():
    return "Connected To Server"

@app.route('/db/<string:db_name>', methods=["GET"])
def getAllFromDB(db_name):
    db = Db(db_name)
    data = {"reply": db.getAllDoc()}
    res = flask.make_response(flask.jsonify(data))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res

@app.route('/sentiment_average', methods=["GET"])
def period_view():
    contents = urllib.request.urlopen("http://127.0.0.1:5984/comp90024/_design/new1/_view/new-view?reduce=true&group_level=1&skip=0").read().decode()
    data = json.loads(contents)
    MapRegion.loadData2Regions(data)
    res = flask.make_response(flask.jsonify(data))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res

if __name__ == '__main__':
    db = Db('tweets')
    app.run(host='0.0.0.0', debug=True)
