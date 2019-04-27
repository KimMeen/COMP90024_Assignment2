import ssl
from geopy.geocoders import Nominatim
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

AustraliaLoc = {}
AustraliaLoc ['longitude'] = [112.92111, 159.109219]
AustraliaLoc ['latitude'] = [ -43.740482, -9.142176]

geolocator = Nominatim(user_agent="gruop66", timeout=10)


def addressToCoordinate(addersss):
    location = geolocator.geocode(addersss)
    if isInsideAustralia(location):
        print(location.latitude, location.longitude)
        return location.latitude, location.longitude
    return None


def isInsideAustralia(location):
    if location is None:
        return False
    if location.longitude > AustraliaLoc['longitude'][0] and \
            location.longitude < AustraliaLoc['longitude'][1] and \
            location.latitude > AustraliaLoc['latitude'][0] and \
            location.latitude < AustraliaLoc['latitude'][1]:
        return True
    return False


