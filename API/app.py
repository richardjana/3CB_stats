from flask import Flask, jsonify, make_response, request
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)

# CORS settings
origin = '*'
headers = ['Content-Type', 'user-name', 'x-api-key']

def check_API_key(headers):
    if (headers.get('x-api-key') is None) or (headers.get('user-name') is None):
        return False

    with open('api_keys.json', 'r') as file:
        api_keys = json.load(file)

    return headers.get('x-api-key') in api_keys[headers.get('user-name')]

@app.route('/hall_of_fame')
@cross_origin(origin=origin, headers=headers)
def hall_of_fame():
    if not check_API_key(request.headers):
        return jsonify({"error": "Unauthorized access"}), 401

    try:
        with open('../data/hall_of_fame.json', 'r') as file:
            return json.load(file)
    except:
        return make_response('An error occurred.', 404)

@app.route('/banned_list')
@cross_origin(origin=origin, headers=headers)
def banned_list():
    if not check_API_key(request.headers):
        return jsonify({"error": "Unauthorized access"}), 401

    try:
        with open('../data/banned_list.json', 'r') as file:
            return json.load(file)
    except:
        return make_response('An error occurred.', 404)

@app.route('/players_rounds_lists')
@cross_origin(origin=origin, headers=headers)
def players_rounds_lists():
    if not check_API_key(request.headers):
        return jsonify({"error": "Unauthorized access"}), 401

    try:
        with open('../data/players_rounds_lists.json', 'r') as file:
            return json.load(file)
    except:
        return make_response('An error occurred.', 404)

@app.route('/round/<int:number>')
@cross_origin(origin=origin, headers=headers)
def round(number):
    if not check_API_key(request.headers):
        return jsonify({"error": "Unauthorized access"}), 401

    try:
        with open(f"../data/rounds/{number}.json", 'r') as file:
            return json.load(file)
    except:
        return make_response('Invalid round number.', 404)

@app.route('/playerstats/<player>')
@cross_origin(origin=origin, headers=headers)
def player_stats(player):
    if not check_API_key(request.headers):
        return jsonify({"error": "Unauthorized access"}), 401

    # TODO: Plot % (Punkteverteilung insgesamt als transparenes Violin Plot hinterlegt?)
    try:
        with open(f"../data/players/{player}.json", 'r') as file:
            return json.load(file)
    except:
        return make_response('Player not found.', 404)

if __name__ == '__main__':
    app.run()
