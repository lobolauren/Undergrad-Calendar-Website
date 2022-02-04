from calendar import c
from pickle import FALSE
import graphviz
from helpers import bool_query_loop, get_course_attr

# testing
import sys
sys.path.insert(0, "./tests/")
from tests.test_constants import PROGRAMS

COLORS = ['blue', 'orange', 'red', 'purple', 'yellow'] # to help visually organize the graph

# Makegraph helper functions
def save_graph_to_pdf(graph: graphviz.Digraph, filename):
    graph.format = 'pdf'
    graph.render(filename=filename, directory="graph-output").replace('\\', '/')


# Since we are dealing with pre-requsites, we want a directed graph (one-way)
def create_course_graph(name, include_legend=True):
    graph = graphviz.Digraph(name)
    graph.attr('graph', ranksep="2")
    if include_legend:
        make_legend(graph)
    return graph


# Change colour of node when course is outside requested department
#   If a MATH course is a prereq for a CIS course, MATH is an "outside course"
def add_outside_department_course(graph:graphviz.Digraph, outside_course):
    graph.node(outside_course, color="red")


# Adding target course to graph
def add_regular_course(graph:graphviz.Digraph, course):
    graph.node(course)


def add_outside_required_courses(graph: graphviz.Digraph, outside_course):
    graph.node(outside_course, color="chocolate4")

# Connecting prereq courses on graph
def add_prereq(graph:graphviz.Digraph, required_course, child_course, color='green'):
    graph.edge(required_course, child_course, color=color)


# Adding equivalent prereqs
def add_eq_prereqs(graph:graphviz.Digraph, eq_prereqs, course, org_name="", degree_program=False):

    course_attr = get_course_attr(course)
    for i, group in enumerate(eq_prereqs):
        for prereq in group:
            if not degree_program:
                if org_name and org_name not in prereq.lower(): # if the course if not in the target course's department
                    add_outside_department_course(graph, prereq)

            add_prereq(graph, prereq, course, color=COLORS[i % len(COLORS)])
            

# Make the Legend for the graph
def make_legend(graph: graphviz.Digraph):
    with graph.subgraph(name='clusterLegend') as legend:
        legend.attr(color="black")
        legend.attr(label="Legend")
    
        add_outside_department_course(legend, "Course Outside of Department")
        add_regular_course(legend, "Course in Department")
        add_outside_required_courses(legend, "Course Outside of Department but Required")
        add_prereq(legend, "Course Outside of Department", "Course in Department", color='black')
        add_prereq(legend, "Course Outside of Department but Required", "Course in Department", color='black')

        add_prereq(legend, "Required Prerequisite", "Course")
        add_prereq(legend, "One of Prerequisite", "Course", color=COLORS[3])
        add_prereq(legend, "One of Prerequisite", "Course", color=COLORS[0])
        add_prereq(legend, "One of Prerequisite", "Course", color=COLORS[1])
        add_prereq(legend, "One of Prerequisite", "Course", color=COLORS[2])


# Building prereq graph for a target course
def parse_prereqs(graph, code, data, org_name):
    print("checking prerequisites...")

    q = [code.upper()]
    visited = set() # courses already added to the graph
    
    navigate_course_queue(graph, data, org_name, q, visited)


# Building a graph for an entire department
def parse_department(graph: graphviz.Digraph, code, data, org_name):
    print("checking department...")
    for course_value in data["courses"][code]:

        add_regular_course(graph, course_value["code"])
        add_eq_prereqs(graph, course_value['prereqs']['eq_prereqs'], course_value['code'], org_name)

        for prereq in course_value["prereqs"]["reg_prereqs"]:
            dep = get_course_attr(prereq)
            if dep != code: # make red - outside course
                add_outside_department_course(graph, prereq)
            add_prereq(graph, prereq, course_value["code"])


# Remove characters that aren't allowed in a filename
def fix_filename(filename):
    bad_chars = ['*', '/', '\\', ':', '\"', '<', '>', '|', '?']
    for c in bad_chars:
        filename = filename.replace(c, '')
    return filename


# Getting name of file to store graph
def get_filename(name):
    filename = name+"-graph"
    filename_query = input("Name graph file? [y/n]: ").strip().lower()

    if filename_query == "y" or filename_query == "yes":
        filename = input("Enter graph name: ").strip()

    filename = fix_filename(filename)
    print("File: "+ filename + " has been created." )
    return filename


# Makes graph given JSON file data
def makegraph(course_data):
    name = input("Course name or department [q to quit]: ").strip().lower()
    
    # allow user to quit
    if name.lower() == 'q' or name.lower() == 'quit':
        return False
    
    course_attr = name
    if '*' in name:
        course_attr = get_course_attr(name)

    # check for valid department

    search_bool = course_attr not in course_data['courses'].keys() and course_attr not in course_data['programs'].keys()

    if search_bool:
        print(name + ' not found.')
        return True

    print("making graph...")
    course_graph = create_course_graph("graph1")
    
    if len(name) > 4 and "*" in name:
        # Creating a graph for a specific course (ex: CIS*3760)
        course_graph.attr(
            label=f'Prerequisite Graph for {name.upper()}',
            labelloc='t',
            fontsize='30'
        )
        parse_prereqs(course_graph, name, course_data, org_name=course_attr)
    else:

        degree_search = False

        if name in course_data["programs"] and name in course_data["courses"]:
            degree_search = bool_query_loop("\nSeach found in both programs & departments? [program/department] ", "[p/d]", ["program", "p"], ["department", "d"])
        elif name in course_data["programs"]:
            degree_search = True

        org_name = name
        # Creating a graph for an entire department (ex: CIS, MATH, ACCT, etc)
        
        if degree_search:
            graph_degree_program(course_graph, name, course_data)
        else:
            course_graph.attr(
                label=f'Prerequisite Graph for all {name.upper()} Courses',
                labelloc='t',
                fontsize='30'
            )
            parse_department(course_graph, name, course_data, org_name)



    save_graph_to_pdf(course_graph, get_filename(name))
    
    return bool_query_loop("\nGraph another course? [y/n] ", "[y/n]", ["yes", "y"], ["no", "n"])

# Graphs all the required pre-requsites and required courses for a desired degree program
# The list of all degree programs is under "programs" in course_info
# Similar to parse_prereqs
def graph_degree_program(graph: graphviz.Digraph, degree_program, course_info):

    print("Graphing Degree Program...")

    # add graph title
    graph.attr(
            label=f'Graph for |{degree_program}| degree program',
            labelloc='t',
            fontsize='30'
        )

    all_courses = course_info["programs"][degree_program.lower()]

    major_courses = all_courses["major_reqs"]
    minor_courses = all_courses["minor_reqs"]

    minor_search = False

    # if both major and minor are found, ask user
    if major_courses and minor_courses:
        minor_search = bool_query_loop("\nSearch for major or minor? [major/minor] ", "[ma/mi]", ["minor", "mi"], ["major", "ma"])

    # default major search
    required_courses = major_courses

    # if a minor search is requested
    if minor_courses and minor_search:
        required_courses = minor_courses
        print(f"Minor in {degree_program}:")
        
        # rename graph
        graph.attr(label=f'Graph for |{degree_program}| minor program')

    else:
        print(f"Major in {degree_program}:")

    # get all the course data for all the required courses
    print(f"Number of required courses for CS: {len(required_courses)}")

    # create the queue
    course_queue = required_courses[:]
    visited = set() # courses already added to the graph
    # add the required courses to the set to begin with (resolves issue with arrows)
    for required_course in required_courses:
        visited.add(required_course)


    while course_queue:
        for _ in range(len(course_queue)):

            course = course_queue.pop(0)

            course_attr = get_course_attr(course)

            for course_value in course_info['courses'][course_attr]:
                if course_value['code'] == course:

                    # show as brown if not a required course
                    if course in required_courses:
                        add_regular_course(graph, course)
                    else:
                        add_outside_required_courses(graph, course)
                    
                    # Adding prereqs to graph
                    for prereq in course_value['prereqs']['reg_prereqs']:
                        add_prereq(graph, prereq, course_value['code'])
                        if prereq not in visited: # only add courses that haven't been visted/added to avoid multiple arrows to the same course
                            visited.add(prereq)
                            course_queue.append(prereq)

                    # Adding equivalent prereqs to graph
                    add_eq_prereqs(graph, course_value['prereqs']['eq_prereqs'], course, degree_program=True)
                    for group in course_value['prereqs']['eq_prereqs']:
                        for prereq in group:
                            if prereq not in visited: # only add courses that haven't been visted/added to avoid multiple arrows to the same course
                                visited.add(prereq)
                                course_queue.append(prereq)

def navigate_course_queue(graph, course_info, department, course_queue, visited):
    while course_queue:
        for _ in range(len(course_queue)):
            course = course_queue.pop(0)
            course_attr = get_course_attr(course)

            for course_value in course_info['courses'][course_attr]:
                if course_value['code'] == course:
                    add_regular_course(graph, course)

                    # Adding prereqs to graph
                    for prereq in course_value['prereqs']['reg_prereqs']:
                        dep = get_course_attr(prereq)
                        if dep != department:  # make red - outside course
                            add_outside_department_course(graph, prereq)
                        add_prereq(graph, prereq, course_value['code'])
                        if prereq not in visited: # only add courses that haven't been visted/added to avoid multiple arrows to the same course
                            visited.add(prereq)
                            course_queue.append(prereq)

                    # Adding equivalent prereqs to graph
                    add_eq_prereqs(graph, course_value['prereqs']['eq_prereqs'], course, department)
                    for group in course_value['prereqs']['eq_prereqs']:
                        for prereq in group:
                            if prereq not in visited: # only add courses that haven't been visted/added to avoid multiple arrows to the same course
                                visited.add(prereq)
                                course_queue.append(prereq)
