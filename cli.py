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
    print("Hit enter to skip skip field")
    while inputFlag:
        name = raw_input("Course search criteria(name): ")
        if name.isalpha() or name == "":
            inputFlag = False
        else:
            print("try again")
    inputFlag = True
    while inputFlag:
        code = raw_input("Course search criteria(code): ")
        inputFlag = False
    inputFlag = True
    while inputFlag:
        term = raw_input("Course search criteria(season/term): ")
        # Season (either S, F, or W)
        if term == 'S' or term == 's' or term == 'F' or term == 'f' or term == 'W' or term == 'w' or term == "":
            inputFlag = False
        else:
            print("try again")
    inputFlag = True
    while inputFlag:
        weight = raw_input("Course search criteria(weight): ")
        # Weight (must be a decimal value)
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
    for k in y["courses"][code[:-4].replace("*","")]:
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
    print("would you like to search again?(1-y, 0-n)")
    search = raw_input()

