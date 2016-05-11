import os
import math
import googlemaps

from models import Request, Result

# allowed difference between target distance and route distance
TOLERANCE = 5

# get api key from environ if present else set it

def _get_client():
    key = os.getenv('GMAPS_KEY', 'YOUR_KEY_HERE')
    return googlemaps.Client(key)

def _distance(p1, p2):
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
    )

def lon_lat_from_tbell(tbell):
    """
    Returns a taco bell's (lng, lat) tuple from the json object.
    Used in sorting things.
    """

    return (tbell['geometry']['location']['lng'],
            tbell['geometry']['location']['lat'])

def haversine_distance(p1, p2):
    """
    Points must be in (lon, lat) coordinates and must start in degrees.
    Haversine formula taken from here:
    http://www.movable-type.co.uk/scripts/latlong.html
    """

    mean_radius_of_earth = 3959 # miles
    p1r = (math.radians(p1[0]), math.radians(p1[1]))
    p2r = (math.radians(p2[0]), math.radians(p2[1]))
    a = (
        math.sin((p1r[1] - p2r[1]) / 2.) ** 2 +
        math.cos(p1r[1]) * math.cos(p2r[1]) *
        math.sin((p1r[0] - p2r[0]) / 2.) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return c * mean_radius_of_earth


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
    lon_lats = [lon_lat_from_tbell(x) for x in tbell_list]
    distances = [
        _distance(start_lon_lat, x) for x in lon_lats
    ]
    min_index, _ = min(enumerate(distances), key=lambda p: p[1])
    return tbell_list[min_index]

def choose_next_tbell(home_lon_lat, start_lon_lat, tbell_list,
                      target_dist, cumul_dist):
    """
    Chooses from among the nearest taco bells not yet visited the next taco
    bell. Tries at each stage to minimize:

    abs( target - (cumulative + next leg + straight back from next) )

    In practice, this leads to preferring longer steps earlier, but not in
    directions that would lead to considerable overshooting on the way back.

    Note that we're not optimizing over bicycling distance here, just
    over distance on the surface of the earth. That's to keep API calls
    down and for speed (probably).
    """

    def score(p):
        return abs(
            target - (cumul_dist + haversine_distance(p, start_lon_lat) +
                      haversine_distance(p, home_lon_lat))
        )


    closest_three_tbells = sorted(
        tbell_list,
        key=lambda x: haversine_distance(start_lon_lat, lon_lat_from_tbell(x))
    )[:3]

    scores = [(score(x), x) for x in closest_three_tbells]

    return sorted(scores, key=lambda x: x[0])[0]
