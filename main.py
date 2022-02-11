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
        command = graph_cli[0]
        arguments = graph_cli[1:]

        if command == 'coursesearch' or 'c' == command:
            print('\nCourse Search')
            while True:
                keep_going = coursesearch(course_info)
                if not keep_going:
                    break

        elif command == 'makegraph' or command == 'm':

            try:
                options = 'dpcCo:'
                optlist, _ = getopt.getopt(arguments, options)
                if not valid_options(optlist, ['-d', '-p', '-c', '-C']):
                    print('only one of [-d, -p, -c, -C]')
                    continue

                print('\nPrerequisite Graph')
                while True:

                    args = {}
                    for opt, val in optlist:
                        if opt == '-d':
                            args['department'] = True
                        if opt == '-p':
                            args['program'] = True
                        if opt == '-c':
                            args['course'] = True
                        if opt == '-C':
                            args['make_catalog'] = True
                        if opt == '-o':
                            args['output_file'] = val

                    keep_going = makegraph(course_info, **args)

                    if not keep_going:
                        break

            except getopt.error as err:
                print(str(err))

        elif command == 'help' or command == 'h':
            help(arguments)

        elif is_quit(command):
            break

        else:
            print('not a valid command, enter `help` for a list of valid commands')


if __name__ == '__main__':
    main()
