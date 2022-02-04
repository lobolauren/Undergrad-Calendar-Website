from typing import List

# Given a full course code (i.e. CIS*3760), return course attr (i.e. cis)
def get_course_attr(course_str: str, upper=False):

    if not "*" in course_str: return course_str

    if upper:
        return course_str[:course_str.index('*')].upper().strip()
    else:
        return course_str[:course_str.index('*')].lower().strip()


def get_course_number(course_str: str):
    return course_str[course_str.index('*')+1:]


# general function that returns true or false based on user input
def bool_query_loop(message_str: str, err_str: str, true_res, false_res):
    while True:

        # strip user input and lowercase it
        res = input(message_str).strip().lower()
        if res in true_res:
            return True
        if res in false_res:
            return False
        
        print(err_str)


# general function that returns user input when valid_func returns true (with the input as an argument)
# valid_func is a function that reuturns true or false
def query_loop(message_str: str, err_str: str, valid_func):
    while True:

        res = input(message_str)
        if valid_func(res):
            return res

        print(err_str)


# Functions to easily access course info 

# get all prereqs from a course
def get_prereqs(course: dict) -> dict:
    try:
        return course['prereqs']
    except KeyError:
        return None

# get reg_prereqs for a course
def get_reg_prereqs(course: dict) -> dict:
    try:
        return course['prereqs']['reg_prereqs']
    except KeyError:
        return None

# get all eq_prereq groups for a course
def get_eq_prereqs(course: dict) -> dict:
    try:
        return course['prereqs']['eq_prereqs']
    except KeyError:
        return None

# get all courses in a specified department
def get_dept_courses(data: dict, dept: str) -> dict:
    try:
        return data['courses'][dept]
    except KeyError:
        return None

# get a specific course given the code
def get_course(data: dict, code: str) -> dict:
    try:
        dept = get_course_attr(code)
        for course in data['courses'][dept]:
            if course['code'] == code.upper():
                return course
    except KeyError:
        return None
    return None

# get a list of all courses
def get_all_courses(data: dict) -> List[dict]:
    courses = []
    try:
        for dept in data['courses']:
            courses.extend(get_dept_courses(data, dept))
    except KeyError:
        return []
    return courses
