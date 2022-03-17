from flask import Flask, redirect, request
from flask_cors import CORS

from course_search import get_course_data, get_course_info, get_courses
from make_graph import make_course_graph
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
    
    # Convert terms string back into list
    terms = get_arg(args, 'terms')
    terms_array = terms.split(",")

    # args ex. /api/courses?name=programming&code=cis*2500&weight=0.25&term=W
    return get_courses(
        name=get_arg(args, 'name'),
        code=get_arg(args, 'code'),
        weight=get_arg(args, 'weight'),
        term=terms_array
    )


@app.route(f'{BASE_URL}/graph/course/<code>')
def get_course_graph(code):
    if '*' in code:
        # in order to keep urls clean we'll remove the * from the course codes
        new_url = f'{BASE_URL}/graph/course/{code.replace("*", "")}'
        return redirect(new_url, code=308)
    else:
        code = make_code_valid(code)
        return make_course_graph(code.lower())


if __name__ == '__main__':
    app.run(host='0.0.0.0')
