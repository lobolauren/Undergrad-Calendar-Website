from unicodedata import name
from cv2 import log
from flask import Flask, redirect, request
from flask_cors import CORS

from course_search import get_course_data, get_course_info, get_courses
from helpers import make_code_valid

import json

BASE_URL = '/api'

app = Flask(__name__)
app.url_map.strict_slashes = False

CORS(app)


@app.route(f'{BASE_URL}')
def hello():
    return 'Hello world!'


@app.route(f'{BASE_URL}/get_course_data', methods=['GET'])
def get_course_data_json():
    return get_course_data()


@app.route(f'{BASE_URL}/course/<code>')
def get_course_json(code: str):
    if '*' in code:
        # in order to keep urls clean we'll remove the * from the course codes
        new_url = f'{BASE_URL}/course/{code.replace("*", "")}'
        return redirect(new_url, code=308)
    else:
        code = make_code_valid(code)
        course_info = get_course_info(code)
        if course_info:
            return course_info, 200
        else:
            return 'course not found', 404

def get_arg(args, arg, default=''):
    return args[arg] if arg in args else default

@app.route(f'{BASE_URL}/courses')
def get_courses_list():
    args = request.args
    # args ex. /api/courses?name=programming&code=cis*2500&weight=0.25&term=W
    return get_courses(
        name=get_arg(args, 'name'),
        code=get_arg(args, 'code'),
        weight=get_arg(args, 'weight'),
        term=get_arg(args, 'term')
    )


@app.route(f'{BASE_URL}/coursestest')
def test():
    return json.dumps([
        {
            "code": 'CIS*3760',
            "name": 'This Course',
            "weight": '1.0',
            "term": 'W',
            "desc": 'String parsing mostly...'
        },
        {
            "code": 'CIS*1000',
            "name": 'Intro to Bees',
            "weight": '1000000.0',
            "term": 'P',
            "desc": 'According to all known laws of aviation, there is no way that a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don\'t care what humans think is impossible.'
        }

    ])


@app.route(f'{BASE_URL}/courses_recieve', methods=['GET', 'POST'])
def log_data():
    print(request.args)
    return 'success'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
