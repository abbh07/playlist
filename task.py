import csv
import json

import requests

# from flask import Flask
# from flask import Response, request

readJSONFilename = "playlist.json"
writeCSVFilename = "playlist.csv"
csvFields = ["index", "id", "Title", "danceability", "energy", "mode", "acousticness", "tempo", "Duration_ms", "Num_sections", "Num_segments"]

URL = "http://127.0.0.1:5000/playlist"

# app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def hello():
#     return "Hello World!"

# @app.route('/playlist/all', methods=['GET'])
# def allPlaylists():
#     data = readFromJSONFile()
#     dataFrame = parseInput(data)
#     return Response(json.dumps(dataFrame), mimetype='application/json')

# @app.route('/playlist/attributes', methods=['GET'])
# def getAttributes():
#     args = request.args
#     title = args.get('title')
#     data = readFromJSONFile()
#     dataFrame = parseInput(data)
#     for i in range(len(dataFrame)):
#         if title == dataFrame[i][2]:
#             res = dataFrame[i]
#             break
#     return Response(json.dumps(res), mimetype='application/json')

# @app.route('/playlist/rating', methods=['PUT'])
# def updateRating():
#     payload = request.get_json()
#     title = payload['title']
#     rating = payload['rating']
#     data = readFromJSONFile()
#     dataFrame = parseInput(data)
#     for i in range(len(dataFrame)):
#         if title == dataFrame[i][2]:
#             dataFrame[i].append(rating)
#             res = dataFrame[i]
#             break
#     writeToCSVFile(dataFrame)
#     return Response(json.dumps(res), mimetype='application/json')

def parseInput(data: dict) -> list:
    """Parse the input dictionary and create a list of lists"""
    csvEntryCount = len(data['id'])
    dataFrame = []
    for i in range(csvEntryCount):
        index = str(i)
        row = [i, data['id'][index], data['title'][index], data['danceability'][index], data['energy'][index], data['mode'][index], data['acousticness'][index], data['tempo'][index], data['duration_ms'][index], data['num_sections'][index], data['num_segments'][index]]
        dataFrame.append(row)
    return dataFrame

def writeToCSVFile(dataFrame: list):
    """Writes the dataframe to a CSV file for visualization"""
    try:
        with open(writeCSVFilename, 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(csvFields)
            writer.writerows(dataFrame)
    except IOError:
        print("The output file could not be read.")

def readFromJSONFile() -> dict:
    """Reads the input JSON file"""
    with open(readJSONFilename, 'r') as jsonFile:
        data = json.loads(jsonFile.read())
    return data

def getPlaylistDict(data: list) -> dict:
    """Creates a dict for the POST request"""
    return {
        "index": data[0],
        "id": data[1],
        "title": data[2],
        "danceability": data[3],
        "energy": data[4],
        "mode": data[5],
        "acousticness": data[6],
        "tempo": data[7],
        "duration_ms": data[8],
        "num_sections": data[9],
        "num_segments": data[10],
        "star_rating": -1
    }

def postDataToMongoDB(dataFrame):
    """POST request to populate data in MongoDB"""
    POST_URL = URL + "/add"
    for i in range(len(dataFrame)):
        data = getPlaylistDict(dataFrame[i])
        r = requests.post(url=POST_URL, json=data)
        print("Status code: ", r.status_code)

def main():
    data = readFromJSONFile()
    dataFrame = parseInput(data)
    writeToCSVFile(dataFrame)
    postDataToMongoDB(dataFrame)

if __name__ == "__main__":
    main()