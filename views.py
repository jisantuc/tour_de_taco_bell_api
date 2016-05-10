import os
import math
import googlemaps

from models import Request, Result

# get api key from environ if present else set it

def _get_client():
    key = os.getenv('GMAPS_KEY', 'YOUR_KEY_HERE')
    return googlemaps.Client(key)

def _distance(p1, p2):
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
    )

def tbell_finder(start_lon_lat, client):
    """
    Returns a list of Taco Bells in a certain radius of the start address.
    Default value is 25 miles.
    """

    # 40233.6 is 25 miles in meters
    response = client.places("taco bell", location=start_lon_lat,
                             radius=40233.6)
    if response['status'] != u'OK':
        return response['results']
    else:
        return 'error -- %s' % response['status']

def nearest_tbell(start_lon_lat, tbell_list):
    lon_lats = [
        (x['geometry']['location']['lng'],
         x['geometry']['location']['lat']) for x in tbell_list
    ]
    distances = [
        _distance(start_lon_lat, x) for x in lon_lats
    ]
    min_index, _ = min(enumerate(distances), key=lambda p: p[1])
    return tbell_list[min_index]
