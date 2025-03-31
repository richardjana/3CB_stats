from flask import Flask, jsonify, make_response, request
from flask_cors import cross_origin
import json

app = Flask(__name__)

# CORS settings
ORIGIN = '*'
header_keys = ['Content-Type', 'user-name', 'x-api-key']

def check_api_key(headers):
    """Try to autheticate the user with their API key.
    Args:
        headers (werkzeug.datastructures.Headers): Headers of the request.
    Returns:
        (bool): True if authetification successful, False otherwise.
    """
    if (headers.get('x-api-key') is None) or (headers.get('user-name') is None):
        app.logger.info('Login failed due to missing username / API key.')
        return False

    with open('api_keys.json', 'r', encoding='utf-8') as file:
        api_keys = json.load(file)

    if headers.get('x-api-key') in api_keys[headers.get('user-name')]:
        app.logger.info('Login in for user %s failed with incorrect API key.',
                        headers.get('user-name'))
        return True

    app.logger.info('Login for user %s successful.', headers.get('user-name'))
    return False

@app.route('/hall_of_fame')
@cross_origin(origin=ORIGIN, headers=header_keys)
def hall_of_fame():
    """Get Hall of Fame data.
    Returns:
        (response): JSON data according to file (see analysis.py).
    """
    if not check_api_key(request.headers):
        return make_response('Unauthorized access', 401)

    app.logger.info('Get %s request from %s.', request.endpoint, request.headers.get('user-name'))

    try:
        with open('data/hall_of_fame.json', 'r', encoding='utf-8') as file:
            return jsonify(json.load(file)), 200
    except FileNotFoundError:
        app.logger.warning('Get Hall of Fame failed!')
        return make_response('An error occurred.', 404)

@app.route('/banned_list')
@cross_origin(origin=ORIGIN, headers=header_keys)
def banned_list():
    """Get lists of banned cards: regular and "Introducing ..." formats.
    Returns:
        (response): JSON data according to file (see analysis.py).
    """
    if not check_api_key(request.headers):
        return make_response('Unauthorized access', 401)

    app.logger.info('Get %s request from %s.', request.endpoint, request.headers.get('user-name'))

    try:
        with open('data/banned_list.json', 'r', encoding='utf-8') as file:
            return jsonify(json.load(file)), 200
    except FileNotFoundError:
        app.logger.warning('Get banned list failed!')
        return make_response('An error occurred.', 404)

@app.route('/players_rounds_lists')
@cross_origin(origin=ORIGIN, headers=header_keys)
def players_rounds_lists():
    """Get lists of available round numbers and player names.
    Returns:
        (response): JSON data according to file (see analysis.py).
    """
    if not check_api_key(request.headers):
        return make_response('Unauthorized access', 401)

    app.logger.info('Get %s request from %s.', request.endpoint, request.headers.get('user-name'))

    try:
        with open('data/players_rounds_lists.json', 'r', encoding='utf-8') as file:
            return jsonify(json.load(file)), 200
    except FileNotFoundError:
        app.logger.warning('Get players and rounds lists failed!')
        return make_response('An error occurred.', 404)

@app.route('/round/<int:number>')
@cross_origin(origin=ORIGIN, headers=header_keys)
def round_details(number):
    """Get detailed information on a single round.
    Args:
        number (int): Number of the round for which to get detailed information.
    Returns:
        (response): JSON data according to file (see analysis.py).
    """
    if not check_api_key(request.headers):
        return make_response('Unauthorized access', 401)

    app.logger.info('Get %s request from %s.', request.endpoint, request.headers.get('user-name'))

    try:
        with open(f"data/rounds/{number}.json", 'r', encoding='utf-8') as file:
            return jsonify(json.load(file)), 200
    except FileNotFoundError:
        app.logger.warning('Get details for round %i failed!', number)
        return make_response('Invalid round number.', 404)

@app.route('/playerstats/<player>')
@cross_origin(origin=ORIGIN, headers=header_keys)
def player_stats(player):
    """Get detailed information on a single player.
    Args:
        player (str): Name of the player for which to get detailed information.
    Returns:
        (response): JSON data according to file (see analysis.py).
    """
    if not check_api_key(request.headers):
        return make_response('Unauthorized access', 401)

    app.logger.info('Get %s request from %s.', request.endpoint, request.headers.get('user-name'))

    try:
        with open(f"data/players/{player}.json", 'r', encoding='utf-8') as file:
            return jsonify(json.load(file)), 200
    except FileNotFoundError:
        app.logger.warning('Get details for round %s failed!', player)
        return make_response('Player not found.', 404)

@app.route('/popular_cards')
@cross_origin(origin=ORIGIN, headers=header_keys)
def popular_cards():
    """Get a sorted list of cards, with number of times played and fraction of all cards being used.
    Returns:
        (response): JSON data according to file (see analysis.py).
    """
    if not check_api_key(request.headers):
        return make_response('Unauthorized access', 401)

    app.logger.info('Get %s request from %s.', request.endpoint, request.headers.get('user-name'))

    try:
        with open('data/popular_cards.json', 'r', encoding='utf-8') as file:
            return jsonify(json.load(file)), 200
    except FileNotFoundError:
        app.logger.warning('Get popular cards list failed!')
        return make_response('An error occurred.', 404)

if __name__ == '__main__':
    app.run()
