import csv
import json

import math
from flask import Flask, Response, request
import requests

app = Flask(__name__)

google_geocoding_api_key = ""
if not google_geocoding_api_key:
    import configparser

    config = configparser.ConfigParser()
    config.read('settings.ini')
    google_geocoding_api_key = config['DEFAULT']['google_geocoding_api_key']

with open("locations.csv") as infile:
    reader = csv.DictReader(infile)
    data = []

    # The CSV is delimited by ", " (with a space) instead of the usual "," (with no space), and so I need to get rid of
    # those spaces below, and I need to add the leading spaces to the row_dict's key names.
    id_to_coffee_shop_data = {int(line['id']): {'id': int(line['id']),
                                                'name': line[' name'].strip(),
                                                'address': line[' address'].strip(),
                                                'latitude': float(line[' latitude'].strip()),
                                                'longitude': float(line[' longitude'].strip())} for line in reader}


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/create', methods=['POST'])
def create():
    post_data = json.loads(request.data.decode("utf-8"))
    largest_existing_id = max(id_to_coffee_shop_data.keys())
    new_id = largest_existing_id + 1
    id_to_coffee_shop_data[new_id] = {
        'name': post_data['name'],
        'address': post_data['address'],
        'latitude': post_data['latitude'],
        'longitude': post_data['longitude']
    }
    return json.dumps({'id': new_id})


@app.route('/read/<int:id>')
def read(id):
    try:
        return json.dumps(id_to_coffee_shop_data[id])
    except KeyError:
        return Response("{'message':'No record was found with that ID.'}", status=404, mimetype='application/json')


@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    try:
        post_data = json.loads(request.data.decode("utf-8"))
        id_to_coffee_shop_data[id] = {
            'id': id,
            'name': post_data['name'],
            'address': post_data['address'],
            'latitude': post_data['latitude'],
            'longitude': post_data['longitude']
        }
        return json.dumps({'message': 'Record updated.'})
    except KeyError:
        return Response("{'message':'No record was found with that ID.'}", status=404, mimetype='application/json')


@app.route('/delete/<int:id>', methods=["POST"])
def delete(id):
    try:
        del id_to_coffee_shop_data[id]
        return json.dumps({'message': 'Record deleted.'})
    except KeyError:
        return Response("{'message':'No record was found with that ID.'}", status=404, mimetype='application/json')


@app.route('/nearest/<address>')
def nearest(address):
    request_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (address, google_geocoding_api_key)
    result_object = requests.get(request_url)
    google_response_data = json.loads(result_object.content.decode('utf-8'))

    location = google_response_data['results'][0]['geometry']['location']

    latitude = float(location['lat'])
    longitude = float(location['lng'])

    nearest_coffee_shop = {}
    for coffee_shop in id_to_coffee_shop_data.values():
        distance_to_this_coffee_shop = math.hypot(latitude - coffee_shop['latitude'], longitude - coffee_shop['longitude'])
        if not nearest_coffee_shop or distance_to_this_coffee_shop < nearest_coffee_shop['distance']:
            nearest_coffee_shop = coffee_shop
            nearest_coffee_shop['distance'] = distance_to_this_coffee_shop

    return json.dumps(nearest_coffee_shop)


if __name__ == "__main__":
    app.run(debug=False)
