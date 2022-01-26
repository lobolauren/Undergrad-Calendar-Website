import json

def makegraph(course_data):
    name = input("Course name or department: ").strip().lower()

    # Course code (ex. CIS*1300 or CIS or 1300)
    inputFlag = True
    while inputFlag:
        print("testing function")
        continueSearch = input("\n Graph another course? [y/n] ")
        if continueSearch.lower() == "n" or continueSearch.lower() == "no":
            return False
        return True
