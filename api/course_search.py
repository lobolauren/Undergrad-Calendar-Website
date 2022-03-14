import json

from helpers import get_course, valid_code

COURSE_INFO_JSON = 'course_info.json';

# function to open JSON file
def get_course_data(filename: str=COURSE_INFO_JSON):
    try:
        with open(filename, 'r') as file:
            data = file.read()
            coursedata = json.loads(data)
    # if the file isnt found, return nothing
    except FileNotFoundError as e:
        return {}
    return coursedata


def get_course_info(code: str):
    if not valid_code(code):
        return {}
    else:
        return get_course(get_course_data(COURSE_INFO_JSON), code)


def get_courses(name, code, weight, term):
    return {
        'name': name,
        'code': code,
        'weight': weight,
        'term': term,
    }