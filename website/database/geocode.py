# geocode.py
# Handles geolocational services
# (c) 2015 Roy Portas

from geopy.geocoders import GoogleV3, Nominatim
from re import findall, compile
from time import sleep

geolocator = None
pattern = compile('([0-9][0-9][0-9][0-9])')

def setup_geocoder():
    global geolocator
    geolocator = GoogleV3()

def lookup_suburb(suburb):
    """Looks up the suburb"""
    results = {}
    try:
        location = geolocator.geocode(suburb + " qld")
        results["latitude"] = location.latitude
        results["longitude"] = location.longitude
        return results
    except Exception as e:
        return None


def geocode_to_postcode(address):
    """Geocodes an address into a suburb"""
    sleep(0.25)
    location = geolocator.geocode(address)
    address = location.address
    results = pattern.findall(address)
    data = {}
    data["latitude"] = location.latitude
    data["longitude"] = location.longitude
    if len(results) > 0:
        data["postcode"] = results[0]
        return data
    else:
        return None

setup_geocoder()

if __name__ == "__main__":
    print(geocode_to_postcode("ashgrove"))
    # print(lookup_suburb("coorparoo"))
