import json

from helpers import get_course, valid_code, get_course_attr, get_course_number, get_dept_courses, get_all_depts

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
    #get all courses
    coursedata = get_course_data(COURSE_INFO_JSON)
    courseList = courses = []

    attr = get_course_attr(code)
    num = get_course_number(code)

    try:
        for dept in coursedata['courses']:
            for course in coursedata['courses'][dept]:
                check = True
                print(course['code'])
                if attr:
                    if get_course_attr(course['code']) not in attr:
                        check = False
                #if num:

                
                #if satisfies all searches add
                if check:
                    courseList.extend(course)
    except KeyError:
        return []


    #for course in courseList:
    #    print(course['code'])

    return json.dumps(courseList)