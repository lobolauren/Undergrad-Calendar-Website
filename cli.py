import json

#function if code name (etc CIS*1300) is not entered 
def courseWithNoCode(data,code,weight,name,term):
    course_list = []
    for course_attr in data["courses"]:
                for course_value in data["courses"][course_attr]:
                    check = True
                    if weight and course_value["weight"] != float(weight):
                            continue
                    if code and code[-4:] not in course_value["code"]:
                            continue
                    if name and name.lower() not in (course_value["name"]).lower():
                            continue
                    if(term):
                        check2 = False
                        for desc in course_value["terms"]:
                            if term.lower() in desc.lower() and term != "":
                                check2 = True
                        if not check2:
                            continue
                    #final output
                    if check and (weight == "" and code=="" and name=="" and term=="")==False :
                        course_list.append(course_value["code"])
    return course_list

#function if code name (etc CIS*1300) is entered as the course level or section (ex: 1300 or cis)
def courseWithOnlyNumAlpha(data,code,weight,name,term):
    course_list = []
    for course_attr in data["courses"]:
                    for course_value in data["courses"][course_attr]:
                        check = True
                        if(weight):
                            if course_value["weight"] != float(weight):
                                continue
                        if code.lower() not in course_value["code"].lower():
                                continue
                        if(name):
                            if name.lower() not in (course_value["name"]).lower():
                                continue                        
                        if(term):
                            check2 = False
                            for desc in course_value["terms"]:
                                if term.lower() in desc.lower() and term != "":
                                    check2 = True
                            if not check2:
                                continue

                        #final output
                        if check:
                            course_list.append(course_value["code"])
    return course_list

#function if code name (etc CIS*1300) is entered in full
def courseWithCode(data,code,weight,name,term):
    course_list = []
    for course_attr in data["courses"][code[:-4].replace("*","").lower()]:
                    check = True
                    if(weight):
                        if course_attr["weight"] != float(weight):
                            continue
                    if(code):
                        if code[-4:] not in course_attr["code"]:
                           continue
                    if(name):
                        if name.lower() not in (course_attr["name"]).lower():
                           continue
                    if(term):
                        check2 = False
                        for p in course_attr["terms"]:
                            if term.lower() in p.lower() and term != "":
                                check2 = True
                        if not check2:
                            continue

                    #final output
                    if check:
                        course_list.append(course_attr["code"])
    return course_list                    

#function running comand line interface
def cli(data):
        final_course_list = [] # list to hold all matching courses
        # User input
        inputFlag = True

        # Course name ("programming", "math", "chemistry")
        while inputFlag:
            name = input("Course name (hit enter to skip field): ")
            if name.isalpha() or name == "":
                inputFlag = False
            else:
                print("Error: name cannot contain numbers")
        inputFlag = True

        # Course code (CIS*1300 or 1300)
        while inputFlag:
            code = input("Course code (hit enter to skip field): ")
            inputFlag = False
        inputFlag = True

        # Season/term (either S, F, or W)
        while inputFlag:
            term = input("Course season/term (hit enter to skip field): ").upper()
            if term == 'S' or term == 'F' or term == 'W' or term == "":
                inputFlag = False
            else:
                print("Valid seasons: S, W, or F")
        inputFlag = True

        # Weight/credit (must be a decimal value)
        while inputFlag:
            weight = input("Course weight (hit enter to skip field): ")
            if len(weight) != 0:
                try:
                    float(weight)
                    inputFlag = False
                except ValueError:
                    print("Valid course weight: 0.25, 0.5, 0.75, 1.0 etc")
                    continue
            else:
                inputFlag = False

        #check for length of code name and if inputted for example cis*1300, cis1300, cis, 1300, or null 
        # add returned list values to  master course list
        if (code) and len(code) > 4:
            final_course_list =  courseWithCode(data,code,weight,name,term)
        elif (code.isnumeric()  and len(code) < 5) or (code.isalpha() and len(code) < 5):
            final_course_list = courseWithOnlyNumAlpha(data,code,weight,name,term)
        else:
            final_course_list = courseWithNoCode(data,code,weight,name,term)

        #check length of list of found courses and print to user
        if len(final_course_list) == 0:
            print("\n\nNo Courses Found\n")
        else:
            print("\n\nCourses Found:\n")
            for x in range(len(final_course_list)):
                print(str(final_course_list[x]) + '\n')

        #Menu ------------------------------------------------------
        continueSearch = input("\n\nSearch again? [y/n] ")
        if continueSearch.lower() == "n" or continueSearch.lower() == "no":
            return False
        else:
            return True
    
#function to open JSON file
def get_course_info():
    file = open("course_info.json", "r") 
    data = file.read()
    coursedata = json.loads(data)
    return coursedata


def main():
    course_info = get_course_info()
    print("\nWelcome to UoG Course Search")
    while True:
        keep_going = cli(course_info)
        if not keep_going:
            break

main()
