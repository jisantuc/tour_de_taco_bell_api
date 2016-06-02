from flask import (
    Flask, url_for, render_template, request, jsonify
)
from flask.ext.cors import CORS
from models import Request, Result, RouteForm
import utils
from errors import AddressNotFoundError, PathFinderError

application = Flask(__name__)
CORS(application)

## Error handlers

@application.errorhandler(AddressNotFoundError)
@application.errorhandler(PathFinderError)
def handle_address_not_found(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@application.route('/')
@application.route('/index')
def index():
    form = RouteForm()
    return render_template('index.html', form=form)

@application.route('/tbell_route', methods=['GET', 'POST'])
def result():
    client = utils.get_client()
    data = request.values.to_dict()
    geocode_result = client.geocode(data['address'])
    if geocode_result:
        res = geocode_result[0]['geometry']
        home_lat_lon = (res['location']['lat'], res['location']['lng'])
    else:
        raise AddressNotFoundError(data['address'], status_code=400)
    target = data['desired_route_distance']
    tbell_list = utils.tbell_finder(home_lat_lon, client)
    target = utils.distance_str_to_miles(target)
    path = utils.choose_tbell_sequence(
        home_lat_lon,
        tbell_list,
        target
    )
    if path:
        path_dict = {'status': 'ok', 'path': path}
    else:
        raise PathFinderError('No path found')
    query_url = utils.path_dict_to_embedded_query(path_dict)
    return render_template('map.html', url=query_url,
                           n_tbells=len(path_dict['path']) - 2)

# TODO
@application.route('/random', methods=['GET'])
def random_route():
    pass

#if __name__ == '__main__':
#    application.run(debug=True)
