import json
from shapely.geometry import shape, Point

# convert the coordinates into region names
def getCoordinateRegion(cooridinate, region_file):
    with open(region_file) as f:
        regions = json.load(f)
        if cooridinate is None:
            return None
        for r in regions['features']:
            s = shape(r['geometry'])
            point = Point(cooridinate[1], cooridinate[0])
            if s.contains(point):
                return r['properties']['Name']
