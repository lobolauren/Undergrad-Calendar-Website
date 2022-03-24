from cv2 import log
from flask import Flask, redirect, request
from flask_cors import CORS

from course_search import get_course_data, get_course_info, get_courses, get_department_courses, get_all_courses, get_program_courses
from make_graph import make_course_graph, make_department_graph, make_major_program_graph, make_minor_program_graph
from helpers import make_code_valid, get_all_programs,get_programs_info

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

@app.route(f'{BASE_URL}/get_programs_list', methods=['GET'])
def get_program_list_json():
    return get_programs_info(get_course_data())


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
        school=get_arg(args,"school"),
        name=get_arg(args, 'name'),
        code=get_arg(args, 'code'),
        weight=get_arg(args, 'weight'),
        term=terms_array
    )

@app.route(f'{BASE_URL}/department')
def get_dept_courses_list():
    args = request.args
    
    # Convert terms string back into list
    terms = get_arg(args, 'terms')
    terms_array = terms.split(",")

    # args ex. /api/department?name=cis
    return get_department_courses(
        name=get_arg(args, 'name'),
    )

@app.route(f'{BASE_URL}/program')
def get_program_courses_list():
    args = request.args
    
    # Convert terms string back into list
    terms = get_arg(args, 'terms')
    terms_array = terms.split(",")

    # args ex. /api/program?name=cis&mom=minor
    return get_program_courses(
        name=get_arg(args, 'name'),
        mom=get_arg(args, 'mom'),
    )

@app.route(f'{BASE_URL}/catalog')
def get_catalog():

    # args ex. /api/catalog
    return get_all_courses()


@app.route(f'{BASE_URL}/graph/<school>/course/<code>')
def get_course_graph(school, code):
    if '*' in code:
        # in order to keep urls clean we'll remove the * from the course codes
        new_url = f'{BASE_URL}/graph/{school}/course/{code.replace("*", "")}'
        return redirect(new_url, code=308)
    else:
        code = make_code_valid(code)
        return make_course_graph(code.lower(), school)


@app.route(f'{BASE_URL}/graph/<school>/department/<code>')
def get_department_graph(school, code):
    return make_department_graph(code.lower(), school)


@app.route(f'{BASE_URL}/graph/program/<code>')
def get_major_program_graph(code):
    return make_major_program_graph(code.lower())


@app.route(f'{BASE_URL}/graph/program/minor/<code>')
def get_minor_program_graph(code):
    return make_minor_program_graph(code.lower())


if __name__ == '__main__':
    app.run(host='0.0.0.0')
