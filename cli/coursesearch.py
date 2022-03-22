import json
from helpers import *


# function if course code (ex. CIS*1300) is entered as the course level or section (ex. 1300 or cis) or if nothing is entered
def get_courses(data, code, weight, name, term):
    course_list = []
    for course_attr in data["courses"]: # Going through all courses in JSON file, reading/storing courses that match user input
        for course_value in data["courses"][course_attr]:

            if weight and course_value["weight"] != float(weight):
                continue
            if code and code not in course_value["code"].lower():
                continue
            if name and name not in course_value["name"].lower():
                continue
            if term and term not in course_value["terms"]:
                continue

            course_list.append(course_value)
    return course_list


# function if code name (ex. CIS*1300) is entered in full or a valid depatment code is entered (faster than full search)
def get_courses_with_code(data, code, weight, name, term):
    course_list = []
    course_attr = get_course_attr(code)
    for course_value in data["courses"][course_attr]:

        if weight and course_value["weight"] != float(weight):
            continue
        if code and code[-4:] not in course_value["code"].lower():
            continue
        if name and name not in course_value["name"].lower():
            continue
        if term and term not in course_value["terms"]:
            continue

        course_list.append(course_value)
    return course_list


# function running comand line interface
def coursesearch(data):

    # Course name (ex. "programming", "math", "chemistry")
    name = input("Course name (hit enter to skip field): ").strip().lower()

    # Course code (ex. CIS*1300 or CIS or 1300)
    
    # returns true if the code is a number, a valid department code, or empty
    def valid_code(s): return True if s == "" or get_course_attr(s) in data["courses"] or s.isdigit() else False
    code = query_loop("Course code/number (hit enter to skip field): ",
                      "Not a valid course code. Format: [code]/[number]/[code]*[number] (ex. cis or 1000 or cis*1000)", valid_code)

    # Term (either S, F, or W)
    valid_term = lambda s: True if s.lower() in ["s", "f", "w", ""] else False
    term = query_loop("Course season/term (hit enter to skip field): ", "Valid seasons: S, W, or F", valid_term).upper()

    # Course Weight (must be a decimal value)
    is_float = lambda s: True if s.replace('.','').isdigit() or s == "" else False
    weight = query_loop("Course weight (hit enter to skip field): ",
                        "Valid course weight: 0.25, 0.5, 0.75, 1.0 etc", is_float)
    
    #ask user whether or not to show course descriptions
    print_desc = bool_query_loop("Show Course Descriptions? [y/n] ", "[y/n]", ["yes", "y"], ["no", "n"])
    
    # check for length of code name and if inputted for example cis*1300, cis1300, cis, 1300, or null
    # get course list depending on user input
    if code and len(code) > 4 or code in data["courses"]: #if we already have a valid code, just search in that section
        final_course_list = get_courses_with_code(data, code, weight, name, term)
    else:
        final_course_list = get_courses(data, code, weight, name, term)

    # check length of list of found courses and print to user
    if len(final_course_list) == 0:
        print("\nNo Courses Found.")
    else:
        print("\nCourses Found:")
        for course in final_course_list:

            print(f"{course['code']} - {course['name']} ( {' '.join(course['terms'])} ) [{course['weight']}]")
            if print_desc:
                print(f"   {course['description']}\n")

    return bool_query_loop("\nSearch again? [y/n] ", "[y/n]", ["yes", "y"], ["no", "n"])
