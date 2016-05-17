from flask import (
    Flask, url_for, render_template, request, jsonify
)
from flask.ext.cors import CORS
from models import Request, Result
import utils
from errors import AddressNotFoundError

app = Flask(__name__)
CORS(app)

## Error handlers

@app.errorhandler(AddressNotFoundError)
def handle_address_not_found(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/tbell_route', methods=['GET'])
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
    path = utils.choose_tbell_sequence(
        home_lat_lon,
        tbell_list,
        target
    )
    return jsonify({'path': path})

# TODO
@app.route('/random', methods=['GET'])
def random_route():
    pass

if __name__ == '__main__':
    app.run(debug=True)
