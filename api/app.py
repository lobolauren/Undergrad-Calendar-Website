from flask import Flask
from flask_cors import CORS
import json

from course_search import get_course_info

BASE_PATH = '/api'

app = Flask(__name__)
CORS(app)

@app.route(f'{BASE_PATH}/')
def hello():
    return 'Hello world!'

@app.route(f'{BASE_PATH}/get_course_data/', methods=['GET'])
def get_course_data_json():
    return get_course_info("course_info.json")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
