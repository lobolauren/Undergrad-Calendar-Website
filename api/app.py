import os
import json
from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello, World!</p>"
    #try:
    #    return send_from_directory()
    #except FileNotFoundError:
    #    abort(404)

# function to open JSON file
def get_course_info(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read()
            coursedata = json.loads(data)

    # if the file isnt found, return nothing
    except FileNotFoundError as e:
        return {}
    return coursedata


@app.route("/get_course_data", methods=['GET'])
def get_course_data_json():
    return get_course_info("course_info.json")
