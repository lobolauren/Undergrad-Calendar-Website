import json
import sys

from coursesearch import coursesearch
from makegraph import makegraph

from helpers import *

# function to open JSON file
def get_course_info(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read()
            coursedata = json.loads(data)
            
    # if the file isnt found, return nothing
    except FileNotFoundError as e:
        return {}
    return coursedata


def main():

    # add command line argument to use custom json file
    json_file = 'course_info.json'
    if len(sys.argv) > 2:
        print('Too many arguments.')
    elif len(sys.argv) > 1:
        json_file = sys.argv[1]

    # if the get_course_info function failed, don't run
    course_info = get_course_info(json_file)
    if not course_info:
        print('File not found, run scraper.py')
        return

    print('Welcome to UoG Course Catalog')
    print('you can enter `help` to see a list of commands and their usage')

    while True:

        # Menu prompt
        graph_cli = input('> ').split()

        if graph_cli[0] == 'coursesearch' or 'c' == graph_cli[0]:
            print('\nCourse Search')
            while True:
                keep_going = coursesearch(course_info)
                if not keep_going:
                    break

        elif graph_cli[0] == 'makegraph' or graph_cli[0] == 'm':
            print('\nPrerequisite Graph')
            while True:
                keep_going = makegraph(course_info)
                if not keep_going:
                    break

        elif graph_cli[0] == 'help' or graph_cli[0] == 'h':
            if len(graph_cli) > 1:
                try:
                    with open(f'help/{graph_cli[1]}.txt') as f:
                        print(f.read())
                except FileNotFoundError as e:
                    print('not a valid command, enter `help` for a list of valid commands')
            else:
                with open('help/default.txt') as f:
                    print(f.read())

        elif is_quit(graph_cli[0]):
            break

        else:
            print('not a valid command, enter `help` for a list of valid commands')


if __name__ == '__main__':
    main()
