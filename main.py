import json
import sys
import getopt

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


def help(args):
    if args:
        try:
            with open(f'help/{args[0]}.txt') as f:
                print(f.read())
        except FileNotFoundError as e:
            print('not a valid command, enter `help` for a list of valid commands')
    else:
        with open('help/default.txt') as f:
            print(f.read())


def valid_options(options, only_one_of) -> bool:
    sum_bools = 0
    for opt, _ in options:
        if opt in only_one_of:
            sum_bools += 1
    return sum_bools < 2


def command_coursesearch(arguments, course_info):
    print('\nCourse Search')
    print('-------------')
    while True:
        keep_going = coursesearch(course_info)
        if not keep_going:
            break


def command_makegraph(arguments, course_info):
    try:
        options = 'd:p:c:Co:'
        optlist, _ = getopt.getopt(arguments, options)
        if not valid_options(optlist, ['-d', '-p', '-c', '-C']):
            print('only one of [-d, -p, -c, -C]')
            return False

        while True:

            args = {
                'department': '',
                'program': '',
                'course': '',
                'make_catalog': '',
                'output_file': '',
            }
            for opt, val in optlist:
                if opt == '-d':
                    args['department'] = val
                if opt == '-p':
                    args['program'] = val
                if opt == '-c':
                    args['course'] = val
                if opt == '-C':
                    args['make_catalog'] = True
                if opt == '-o':
                    args['output_file'] = val

            keep_going = makegraph(course_info, **args)
            if not keep_going:
                break

    except getopt.error as err:
        print(str(err))


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

    print('Welcome to University Course Utility')
    print('you can enter `help` to see a list of commands and their usage')

    while True:

        # Menu prompt
        graph_cli = input('> ').split()
        command = graph_cli[0]
        arguments = graph_cli[1:]

        if command == 'coursesearch' or 'c' == command:
            if not command_coursesearch(arguments, course_info):
                continue

        elif command == 'makegraph' or command == 'm':
            if not command_makegraph(arguments, course_info):
                continue

        elif command == 'help' or command == 'h':
            help(arguments)

        elif is_quit(command):
            break

        else:
            print('not a valid command, enter `help` for a list of valid commands')


if __name__ == '__main__':
    main()
