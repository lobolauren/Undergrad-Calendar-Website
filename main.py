import json
from coursesearch import coursesearch
from makegraph import makegraph
# function to open JSON file
def get_course_info(filename):
    try:
        with open(filename, "r") as file:
            data = file.read()
            coursedata = json.loads(data)
            
    # if the file isnt found, return nothing
    except FileNotFoundError as e:
        return {}
    return coursedata


def main():
     # if the get_course_info function failed, don't run
    course_info = get_course_info("course_info.json")

    if not course_info:
        print("\nFile not found, run scraper.py")
        return

    print("Welcome to UoG Course Catalog")
    while True:
        graph_cli = input("[makegraph/coursesearch] >")
        if graph_cli == 'coursesearch':
            print("\nCourse Search")

            while True:
                keep_going = coursesearch(course_info)
                if not keep_going:
                    break
        if graph_cli == 'makegraph':
            print("\n Prerequisite Graph")

            while True:
                keep_going = makegraph(course_info)
                if not keep_going:
                    break
        if graph_cli == 'quit':
            break
if __name__ == '__main__':
    main()
