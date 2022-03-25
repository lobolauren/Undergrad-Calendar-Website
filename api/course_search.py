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

#returns dict of courses with the given paraemeters(which can have no data in the call)
def get_courses(school, name, code, weight, term):
    #get all courses
    if school != "guelph":
        jsonfile = 'course_info_carleton.json'
    else:
        jsonfile=COURSE_INFO_JSON

    coursedata = get_course_data(jsonfile)
    courseList = []

    try:
        attr = get_course_attr(code)
        num = get_course_number(code)

        for dept in coursedata['courses']:
            for course in coursedata['courses'][dept]:
                check = True

                #name
                if name:
                    if name.lower() not in course['name'].lower():
                        check = False

                #code
                if attr:
                    if get_course_attr(course['code']) not in attr:
                        check = False
                if num:
                    if get_course_number(course['code']) not in num:
                        check = False
                
                #weight
                if weight in "0.25":
                    if course['weight'] != 0.25:
                        check = False
                elif weight in "0.5":
                    if course['weight'] != 0.5:
                        check = False
                elif weight in "0.75":
                    if course['weight'] != 0.75:
                        check = False
                elif weight in "1.0":
                    if course['weight'] != 1.0:
                        check = False

                #term
                termcheck = False
                if len(term) == 2:
                    for t in course['terms']:
                        if t.upper() in term[0].upper() or t.upper() in term[1].upper():
                            termcheck = True
                elif len(term) == 1:
                    for t in course['terms']:
                        if t.upper() in term[0].upper():
                            termcheck = True
                else:
                    termcheck = True
                
                if not termcheck:
                    check = False
                    
                
                #if satisfies all searches add
                if check:
                    print(course['code'])
                    courseList.append(course)
    except KeyError:
        return []

    return json.dumps(courseList)

def get_department_courses(name):
    #get all courses
    coursedata = get_course_data(COURSE_INFO_JSON)
    courseList = []

    try:
        attr = get_course_attr(name)

        for dept in coursedata['courses']:
            if dept in attr:
                for course in coursedata['courses'][dept]:
                    #print(course['code'])
                    courseList.append(course)
    except KeyError:
        return []

    return json.dumps(courseList)

def get_program_courses(name, mom):
    #get all courses
    coursedata = get_course_data(COURSE_INFO_JSON)
    programList = []
    courseList = []

    try:
        attr = get_course_attr(name)

        for program in coursedata['programs']:
            if program in attr:
                if mom.lower() in "minor":
                    #print(coursedata['programs'][program]["minor_reqs"])
                    programList = coursedata['programs'][program]["minor_reqs"]
                    courseList = coursedata['programs'][program]["minor_extras"]
                if mom.lower() in "major":
                    #print(coursedata['programs'][program]["major_reqs"])
                    programList = coursedata['programs'][program]["major_reqs"]
                    courseList = coursedata['programs'][program]["major_extras"]

        for course in programList:
            #print(get_course_info(course))
            courseList.append(get_course_info(course))

    except KeyError:
        return []

    return json.dumps(courseList)

def get_all_courses():
    #get all courses
    coursedata = get_course_data(COURSE_INFO_JSON)
    courseList = []

    try:
        for dept in coursedata['courses']:
                for course in coursedata['courses'][dept]:
                    #print(course['code'])
                    courseList.append(course)
    except KeyError:
        return []

    return json.dumps(courseList)

