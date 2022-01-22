import json

f = open("ex.json", "r")
x = f.read()
y = json.loads(x)

search = True
while search:
    # Reset flags
    correct_input = 0
    incorrect_coursesearch = False

    # User input
    inputFlag = True
    print("Welcome to UoG Course Search")

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
        term = input("Course season/term (hit enter to skip field): ")
        if term == 'S' or term == 's' or term == 'F' or term == 'f' or term == 'W' or term == 'w' or term == "":
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
                continue
        else:
            inputFlag = False

    check = True
    print("\n\nCourses Found:")
    for k in y["courses"][code[:-4].replace("*","").lower()]:
        check = True
        #print(k.keys())

        if k.get("weight") != float(weight) and weight != "":
            #print("weight")
            check = False
        elif code[-4:] not in k.get("code") and code != "":
            #print("code")
            check = False
        elif name.lower() not in (k.get("name")).lower() and name != "":
            #print("name")
            check = False

        check2 = False
        for j in k.get("terms"):
            if term.lower() in j.lower() and term != "":
                check2 = True

        if not check2:
            check = False

        #final output
        if check:
            print(k.get("code"))


    #Menu ------------------------------------------------------
    continueSearch = input("Search again?[y/n]")
    if continueSearch.lower() == "n":
        search = False
