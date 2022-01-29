import json

# function if course code (ex. CIS*1300) is not entered
def get_courses_without_code(data, weight, name, term):
    course_list = []
    for course_attr in data["courses"]:
        for course_value in data["courses"][course_attr]:

            if weight and course_value["weight"] != float(weight):
                continue
            if name and name.lower() not in (course_value["name"]).lower():
                continue
            if term and term not in course_value["terms"]:
                continue

            course_list.append(course_value)
    return course_list


# function if course code (ex. CIS*1300) is entered as the course level or section (ex. 1300 or cis)
def get_courses_with_partial_code(data, code, weight, name, term):
    course_list = []
    for course_attr in data["courses"]:
        for course_value in data["courses"][course_attr]:

            if weight and course_value["weight"] != float(weight):
                continue
            if code not in course_value["code"].lower():
                continue
            if name and name not in course_value["name"].lower():
                continue
            if term and term not in course_value["terms"]:
                continue

            course_list.append(course_value)
    return course_list


# function if code name (ex. CIS*1300) is entered in full
def get_courses_with_code(data, code, weight, name, term):
    course_list = []
    course_attr = code[:code.index('*')].lower()
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
        break  # only ever going to be one course so no need to keep looking
    return course_list


# function running comand line interface
def coursesearch(data):

    # Course name (ex. "programming", "math", "chemistry")
    name = input("Course name (hit enter to skip field): ").strip().lower()

    # Course code (ex. CIS*1300 or CIS or 1300)
    input_flag = True
    error_msg = "Not a valid course code. Format: [code]/[number]/[code]*[number] (ex. cis or 1000 or cis*1000)"
    while input_flag:
        code = input(
            "Course code/number (hit enter to skip field): ").strip().lower()
        # check formatting of input for course code
        if code == "":
            input_flag = False
        elif "*" in code:
            # check formatting of full course code (IE: CIS*1300)
            dept, num = code.split('*')
            if dept not in data['courses'].keys() or len(num) != 4 or not num.isnumeric():
                print(error_msg)
            else:
                input_flag = False
        elif len(code) > 4:
            print(error_msg)
        elif len(code) < 5 and not code.isnumeric() and code not in data['courses'].keys():
            print(error_msg)
        elif code.isnumeric() and len(code) != 4:
            print(error_msg)
        else:
            input_flag = False

    # Term (either S, F, or W)
    input_flag = True
    while input_flag:
        term = input(
            "Course season/term (hit enter to skip field): ").strip().upper()
        if term == 'S' or term == 'F' or term == 'W' or term == "":
            input_flag = False
        else:
            print("Valid seasons: S, W, or F")

    # Course Weight (must be a decimal value)
    input_flag = True
    while input_flag:
        weight = input("Course weight (hit enter to skip field): ").strip()
        if len(weight) != 0:
            try:
                float(weight)
                input_flag = False
            except ValueError:
                print("Valid course weight: 0.25, 0.5, 0.75, 1.0 etc")
                continue
        else:
            input_flag = False

    #ask user whether or not to show course descriptions
    print_desc = False
    print_desc_query = input("Show Course Descriptions? [y/n] ").lower()
    if print_desc_query == "y" or print_desc_query == "yes":
        print_desc = True

    # check for length of code name and if inputted for example cis*1300, cis1300, cis, 1300, or null
    # get course list depending on user input
    if code and len(code) > 4:
        final_course_list = get_courses_with_code(
            data, code, weight, name, term)
    elif code and len(code) < 5:
        final_course_list = get_courses_with_partial_code(
            data, code, weight, name, term)
    else:
        final_course_list = get_courses_without_code(
            data, weight, name, term)

    # check length of list of found courses and print to user
    if len(final_course_list) == 0:
        print("\nNo Courses Found.")
    else:
        print("\nCourses Found:")
        for course in final_course_list:

            print(f"{course['code']} - {course['name']} ( {' '.join(course['terms'])} ) [{course['weight']}]")
            if print_desc:
                print(f"   {course['description']}\n")

    continue_search = input("\nSearch again? [y/n] ").strip().lower()
    if continue_search == "n" or continue_search == "no":
        return False
    return True


