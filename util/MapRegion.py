import json
import Server
from shapely.geometry import shape, Point

with open('aus_regions.json') as f:
    regions = json.load(f)

# retrieve the score from db view, write it into a file for map data to load
def loadData2Regions(data):
    for r in regions['features']:
        value = getPlaceValue(data, r['properties']['Name'])
        r['sentiment_score'] = value
    with open("../WebPage/regionsData.json","w") as out:
        out.write("var statistic = "+json.dumps(regions))

# get the related value of the place
def getPlaceValue(regions, regionName):
    if regions is None:
        return None
    for i in regions['rows']:
        if i['key'] == regionName:
            return i['value']
    return None

# convert the coordinates into region names
def getCoordinateRegion(cooridinate):
    if cooridinate is None:
        return None
    for r in regions['features']:
        s = shape(r['geometry'])
        point = Point(cooridinate[1], cooridinate[0])
        if s.contains(point):
            return r['properties']['Name']
