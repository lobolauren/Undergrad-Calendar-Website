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
def cli(data):

    # Course name (ex. "programming", "math", "chemistry")
    name = input("Course name (hit enter to skip field): ").strip().lower()

    # Course code (ex. CIS*1300 or CIS or 1300)
    inputFlag = True
    while inputFlag:
        code = input(
            "Course code/number (hit enter to skip field): ").strip().lower()
        if code == "":
            inputFlag = False
        elif "*" in code:
            dept, num = code.split('*')
            if dept not in data['courses'].keys() or len(num) != 4 or not num.isnumeric():
                print(
                    "Not a valid course code. Format: [code]/[number]/[code]*[number] (ex. cis or 1000 or cis*1000)")
            else:
                inputFlag = False
        elif len(code) > 4:
            
            print("Not a valid course code. Format: [code]/[number]/[code]*[number] (ex. cis or 1000 or cis*1000)")

        elif len(code) < 5 and not code.isnumeric() and code not in data['courses'].keys():

            print("Not a valid course code. Format: [code]/[number]/[code]*[number] (ex. cis or 1000 or cis*1000)")

        elif code.isnumeric() and len(code) != 4:

            print("Not a valid course code. Format: [code]/[number]/[code]*[number] (ex. cis or 1000 or cis*1000)")
            
        else:
            inputFlag = False

    # Term (either S, F, or W)
    inputFlag = True
    while inputFlag:

        term = input(
            "Course season/term (hit enter to skip field): ").strip().upper()

        if term == 'S' or term == 'F' or term == 'W' or term == "":
            inputFlag = False
        else:
            print("Valid seasons: S, W, or F")

    # Course Weight (must be a decimal value)
    inputFlag = True
    while inputFlag:

        weight = input("Course weight (hit enter to skip field): ").strip()
        if len(weight) != 0:

            try:
                float(weight)
                inputFlag = False
            except ValueError:
                print("Valid course weight: 0.25, 0.5, 0.75, 1.0 etc")
                continue

        else:
            inputFlag = False

    # check for length of code name and if inputted for example cis*1300, cis1300, cis, 1300, or null
    # get course list depending on user input
    if code and len(code) > 4:

        final_course_list = get_courses_with_code(
            data, code, weight, name, term)

    elif code and len(code) < 5:

        final_course_list = get_courses_with_partial_code(
            data, code, weight, name, term)

    else:
        final_course_list = get_courses_without_code(data, weight, name, term)

    # check length of list of found courses and print to user
    if len(final_course_list) == 0:
        print("\nNo Courses Found.")
    else:
        print("\nCourses Found:")

        #ask user whether or not to show course descriptions
        print_desc = False

        print_desc_query = input("Show Course Descriptions? [y/n] ")
        if print_desc_query.lower() == "y" or print_desc_query.lower() == "yes":
            print_desc = True

        for course in final_course_list:

            #put list of terms into a readable format
            term_str = "( "
            for term in course["terms"]:
                term_str += term + " "
            term_str += ")"

            #print course info
            print('\n', course['code'], course['name'],
                  term_str, '[',course['weight'],']')
            
            #print description
            if print_desc:
                print('\t', course['description'])
            print() #extra newline

    continueSearch = input("\nSearch again? [y/n] ")
    if continueSearch.lower() == "n" or continueSearch.lower() == "no":
        return False
    return True


# function to open JSON file
def get_course_info(filename):
    try:
        with open(filename, "r") as file:
            data = file.read()
            coursedata = json.loads(data)
            
    #if the file isnt found, return nothing
    except FileNotFoundError as e:
        return {}
    return coursedata


def main():

    course_info = get_course_info("course_info.json")
    
    #if the get_course_info function failed, don't run
    if not course_info:
        print("\nFile not found, run scraper.py")
        return

    print("\nWelcome to UoG Course Search")

    while True:
        keep_going = cli(course_info)
        if not keep_going:
            break


if __name__ == '__main__':
    main()
