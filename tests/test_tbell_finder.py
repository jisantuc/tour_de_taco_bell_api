from ..utils import (
    nearest_tbell, haversine_distance
)

tbells = [
    {u'formatted_address': (u'2951 Market St, Philadelphia, PA 19104,',
                            ' United States'),
     u'geometry': {u'location': {u'lat': 39.9556108, u'lng': -75.1820022}},
     u'icon': (u'https://maps.gstatic.com/mapfiles/place_api/icons/'
               'restaurant-71.png'),
     u'id': u'9ce343982cac378423e1b7e79d3600bc0b3afd17',
     u'name': u'Pizza Hut',
     u'opening_hours': {u'open_now': True, u'weekday_text': []},
     u'place_id': u'ChIJcx1iQUnGxokRtA7lPzcGssg',
     u'price_level': 1,
     u'reference': (u'CmRdAAAAqUB5cdm_8X7lWtjM8VEmEA6n55_xoxgykk3CVTwbfpqYtA5',
                    'zPZ2VtgS7SfKKEa3R3hcoKtPwk_8CUyK6jA0pYeXfHu0hvHGhgFUeE88',
                    'mySEVSeTyLqpiAC1xtjzaAz9SEhAPi6XUI2AK3gY7f-gTrhRvGhSzzXk',
                    '-YQwhENXxA3GEVr5p4NxLYQ'),
     u'types': [u'meal_delivery',
                u'restaurant',
                u'food',
                u'point_of_interest',
                u'establishment']},
    {u'formatted_address': (u'3032 N Broad St, Philadelphia, PA ',
                            '19132, United States'),
     u'geometry': {u'location': {
         u'lat': 39.999774, u'lng': -75.15368699999999
     }},
     u'icon': (u'https://maps.gstatic.com/mapfiles/place_api/icons/restaurant',
               '-71.png'),
     u'id': u'c06ce3c118f1ee6f1de7e6b42c0ddceb47c5a74c',
     u'name': u'Taco Bell',
     u'opening_hours': {u'open_now': True, u'weekday_text': []},
     u'place_id': u'ChIJrYnskf-3xokRcAC7Fhtmom4',
     u'price_level': 1,
     u'rating': 3.2,
     u'reference': (u'CmRcAAAA-aYXPruidGs8Ow27JFStMrOJTUTJIg1EFIDexeHGSQoaEE0',
                    'NQm3fHa55KGwjEJyvzhphWe-PqrBwTxP-ZMUC0e4llr5DsPw2FLrcx49',
                    'PdvPCruO6rocjDlpVeP2N6LhUEhDZ0N5U05sadfj2DDwO6zApGhRWP5J',
                    'V34EswulgzbDko_08JJRKjw'),
     u'types': [
         u'restaurant', u'food', u'point_of_interest', u'establishment'
     ]}
]

def test_distance(tbells=tbells):
    start = (39.951, -75.210149)
    assert nearest_tbell(start, tbells) == tbells[0]

def test_haversine():
    """
    Result from http://www.movable-type.co.uk/scripts/latlong.html for
    (-75.210149, 39.951) to (-75.153687, 39.999774), after conversion
    to miles:

    4.505
    """

    p1 = (39.951, -75.210149)
    p2 = (39.999774, -75.153687)

    assert round(haversine_distance(p1, p2), 3) == 4.505
