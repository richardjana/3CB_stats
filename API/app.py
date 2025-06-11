from io import BytesIO
import json
import logging

from flask import Flask, jsonify, make_response, request, send_file
from flask_cors import cross_origin
from PIL import Image, ImageDraw, ImageFont
import requests

app = Flask(__name__)

# CORS settings
ORIGIN = '*'
header_keys = ['Content-Type', 'user-name', 'x-api-key']

# logger settings
handler = logging.FileHandler('app.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

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

def get_card_image(card_name):
    # get list of prints
    response = requests.get(f"https://api.scryfall.com/cards/named?exact={card_name}", stream=True)
    if response.status_code == 200:
        prints_uri = response.json()['prints_search_uri']

    # get image of oldest print
    response = requests.get(prints_uri, stream=True)
    if response.status_code == 200:
        img_uri = response.json()['data'][-1]['image_uris']['art_crop']

    response = requests.get(img_uri, stream=True)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))

@app.route('/badge/<player>.png')
@cross_origin(origin=ORIGIN, headers='Content-Type')
def badge(player: str):
    """ Create a badge to use on social media for the player.
    Args:
        player (str): Name of the player.
    Returns:
        (file): Badge image.
    """
    with open('data/players_rounds_lists.json', 'r', encoding='utf-8') as file:
        player_list = json.load(file)['player_names']

    if player not in player_list:
        return make_response('Player does not exist', 404)

    image = Image.new('RGB', (600, 125), color='#888')
    draw = ImageDraw.Draw(image)

    with open(f"data/players/{player}.json", 'r', encoding='utf-8') as file:
        top3_cards = [entry['card'] for entry in json.load(file)['cards'][:3]]

    fetched_image = get_card_image(top3_cards[0])
    fetched_image.thumbnail((100, 100))  # Resize if needed (max sizes)
    image.paste(fetched_image, (180, 10))  # Paste onto the badge

    # Load a font (make sure to have a .ttf file in your directory or use a default one)
    try:
        font = ImageFont.truetype('arial.ttf', 16)
    except IOError:
        font = ImageFont.load_default()

    # Draw badge information
    draw.text((10, 10), f"Badge: {player}", font=font, fill="black")
    draw.text((10, 40), f"some other text", font=font, fill="black")

    # Optionally, add a badge image if you have a specific one
    # badge_image = Image.open(requests.get(badge['image_url'], stream=True).raw)
    # image.paste(badge_image, (180, 50))

    # Convert image to byte stream and return as response
    byte_io = BytesIO()
    image.save(byte_io, 'PNG')
    byte_io.seek(0)

    return send_file(byte_io, mimetype='image/png')

@app.route('/badge_embedding/<player>')
@cross_origin(origin=ORIGIN, headers='Content-Type')
def badge_embedding(player: str):
    """ Provide embedding HTML code for the badge.
    Args:
        player (str): Name of the player.
    Returns:
        (responce): The HTML embedding code.
    """
    embed_code = f'<img src="{request.host_url}badge/{player}.png" alt="3CB_stats info badge">'
    return jsonify({'embed_code': embed_code}), 200

if __name__ == '__main__':
    app.run()
