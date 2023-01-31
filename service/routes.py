import json
import os

from flask import Response, request
from pymodm.connection import connect
from pymongo import MongoClient

from service.models import Playlist

from . import app

# Get Database URI from env if present
DATABASE_URI = os.getenv("DATABASE_URI", "mongodb://localhost:27017/playlist")
client = MongoClient(DATABASE_URI) 
connect(DATABASE_URI)

@app.route("/", methods=['GET'])
def index():
    """Base URL for the app"""
    app.logger.info("Request for Base URL")
    return "Base URL"

@app.route('/playlist/all', methods=['GET'])
def allPlaylists():
    """Retrieves all the playlists"""
    app.logger.info("Request for list of all playlists")
    playlist_array = Playlist.findAll()
    results = []
    for document in playlist_array:
        results.append(document.serialize())
    app.logger.info("Returning %d playlists", playlist_array.count())
    return Response(json.dumps(results), mimetype='application/json')

@app.route('/playlist/attributes', methods=['GET'])
def getAttributes():
    """Gets a playlist by title"""
    app.logger.info("Request for playlist with title")
    args = request.args
    # TODO: error check
    title = args.get('title')
    playlist = Playlist.find(title)
    app.logger.info("Fetched playlist with title %s:  %s", title, playlist.serialize())
    return Response(json.dumps(playlist.serialize()), mimetype='application/json')

@app.route('/playlist/rating', methods=['PUT'])
def updateRating():
    """Updates the rating for a playlist"""
    app.logger.info("Request for updating star rating")
    payload = request.get_json()
    # TODO: error check
    title = payload['title']
    rating = payload['rating']
    playlist = Playlist.update(title, rating)
    app.logger.info("Star rating updated: %s", playlist.serialize())
    return Response(json.dumps(playlist.serialize()), mimetype='application/json')

@app.route('/playlist/add', methods=['POST'])
def createPlaylist():
    """Creates playlist"""
    app.logger.info("Request for adding a playlist")
    payload = request.get_json()
    # TODO: error check
    app.logger.info(payload)
    playlist = Playlist()
    data = playlist.deserialize(payload)
    data.save()
    app.logger.info("Data saved: %s", data.serialize())
    return Response(json.dumps(data.serialize()), mimetype='application/json')
