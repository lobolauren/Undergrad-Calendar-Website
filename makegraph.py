from calendar import c
import graphviz
from helpers import bool_query_loop, get_course_attr, get_reg_prereqs, get_eq_prereqs

COLORS = ['blue', 'orange', 'red', 'purple', 'yellow'] # to help visually organize the graph

# Makegraph helper functions
def save_graph_to_pdf(graph: graphviz.Digraph, filename):
    graph.format = 'pdf'
    graph.render(filename=filename, directory="graph-output").replace('\\', '/')


# Make the Legend for the graph
def make_legend(graph: graphviz.Digraph):
    # try to make a graph
    with graph.subgraph(name='clusterLegend') as legend:
        legend.attr(
            color="black",
            label="Legend",
            style="filled",
            fillcolor="azure"
        )

        # department/degree exceptions
        # first creates nodes, then connects them with add_prereq
        add_outside_department_course(legend, "Course Outside of Department")
        add_regular_course(legend, "Course in Department")
        add_outside_required_courses(legend, "Course not required by degree program")
        add_prereq(legend, "Course Outside of Department", "Course in Department", color='black')
        add_prereq(legend, "Course not required by degree program", "Course in Department", color='black')

        # prerequisites examples
        add_prereq(legend, "Required Prerequisite", "Course")
        add_prereq(legend, "One of Prerequisite", "Course", color=COLORS[3])
        add_prereq(legend, "One of Prerequisite", "Course", color=COLORS[0])
        add_prereq(legend, "One of Prerequisite", "Course", color=COLORS[1])
        add_prereq(legend, "One of Prerequisite", "Course", color=COLORS[2])

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
    graph.node(outside_course, color="salmon", style="filled", fillcolor="lightgray", shape="rect")


# Adding target course to graph
def add_regular_course(graph:graphviz.Digraph, course):
    graph.node(course, style="filled", fillcolor="aliceblue")


def add_outside_required_courses(graph: graphviz.Digraph, outside_course):
    graph.node(outside_course, color="chocolate4", style="filled", fillcolor="lightgray", shape="rect")

# Connecting prereq courses on graph
def add_prereq(graph:graphviz.Digraph, required_course, child_course, color='green'):
    graph.edge(required_course, child_course, color=color)


# Adding equivalent prereqs
def add_eq_prereqs(graph:graphviz.Digraph, eq_prereqs, course, org_name="", degree_program=False):

    course_attr = get_course_attr(course)
    for i, group in enumerate(eq_prereqs):
        for prereq in group:
            # if the course if not in the target course's department
            if (not degree_program) and org_name and (org_name not in prereq.lower()):
                add_outside_department_course(graph, prereq)

            add_prereq(graph, prereq, course, color=COLORS[i % len(COLORS)])
            

# Building prereq graph for a target course
def parse_prereqs(graph, code, data, org_name):
    print("checking prerequisites...")

    q = [code.upper()]
    visited = set() # courses already added to the graph
    
    navigate_course_queue(graph, data, q, visited, org_name)


# Building a graph for an entire department
def parse_department(graph: graphviz.Digraph, code, data, org_name):
    print("checking department...")

    # for each course with the matching course code
    for course_value in data["courses"][code]:
        # create the node for that course then add all eq_prerequisites
        add_regular_course(graph, course_value["code"])
        add_eq_prereqs(graph, get_eq_prereqs(course_value), course_value['code'], org_name)

        #adding regular prerequisites
        for prereq in get_reg_prereqs(course_value):
            dep = get_course_attr(prereq)
            if dep != code: # make red - outside course
                add_outside_department_course(graph, prereq)
            add_prereq(graph, prereq, course_value["code"])


# Graphs all the required pre-requsites and required courses for a desired degree program
# The list of all degree programs is under "programs" in course_info.json
def graph_degree_program(graph: graphviz.Digraph, degree_program, course_info):
    print("Graphing Degree Program...")

    #full degree object within programs
    all_courses = course_info["programs"][degree_program.lower()]

    bachelor = all_courses['bachelor']
    title = all_courses['title']

    # add graph title
    graph.attr(
            label=f'{bachelor}: {title} - major',
            labelloc='t',
            fontsize='30'
        )
    # list all major and minor courses
    major_courses = all_courses["major_reqs"]
    minor_courses = all_courses["minor_reqs"]

    # if minor_courses is empty, minor_search is false
    minor_search = minor_courses

    # if both major and minor are found, ask user
    if major_courses and minor_courses:
        minor_search = bool_query_loop("\nSearch for major or minor? [major/minor] ", "[ma/mi]", ["minor", "mi"], ["major", "ma"])

    # default major search
    required_courses = major_courses[:]

    # if a minor search is requested
    if minor_search:
        required_courses = minor_courses[:]
        print(f"Minor in {degree_program}:")
        
        # rename graph
        graph.attr(label=f'{bachelor}: {title} - minor',)

    else:
        print(f"Major in {degree_program}:")

    # get all the course data for all the required courses
    print(f"Number of required courses: {len(required_courses)}")

    # create the queue
    course_queue = required_courses[:]
    visited = set() # courses already added to the graph
    # add the required courses to the set to begin with (resolves issue with arrows)
    for required_course in required_courses:
        visited.add(required_course)

    # adds all the required courses, pre-reqs, and equivalent prereqs into the graph
    navigate_course_queue(graph, course_info, course_queue, visited, graph_degree_program=True, required_courses=required_courses)



# Department is specified when working with parse_prereqs (which graphs for a single course + its prerequsites)
# When graphing a degree program, department is skipped and graph_degree_program + required_courses are passed in
# graph is the graph, course_info is the data structure containing degrees, prerequisistes, etc., visited is a set of courses that have already been added to the graph,
# department is the course_attr for the current department, set graph_degree_programs to true if the graph is for a program, required courses is a list of courses for the degree
def navigate_course_queue(graph, course_info, course_queue, visited, department="", graph_degree_program=False, required_courses=[]):

    # until the queue is empty
    while course_queue:

        # do this for each course in the course queue
        for _ in range(len(course_queue)):
            # This process adds the popped course to the graph
            course = course_queue.pop(0)
            course_attr = get_course_attr(course)

            # find the course in the list of courses for the department
            for course_value in course_info['courses'][course_attr]:
                if course_value['code'] == course:

                    # if graph is for degree program and the course being added is not required for the degree
                    if course not in required_courses and graph_degree_program:
                        add_outside_required_courses(graph, course) # Colours outside courses brown
                    else:
                        add_regular_course(graph, course) # Coloured as black

                    # add prereqs for the curent course to the graph
                    for prereq in get_reg_prereqs(course_value):
                        # get department code for the prereq
                        prereq_dep = get_course_attr(prereq)
                        
                        # only done for graphing single course
                        if not graph_degree_program and prereq_dep != department:  # make red - outside course
                            add_outside_department_course(graph, prereq)

                        add_prereq(graph, prereq, course_value['code'])
                        
                        # only add courses that haven't been visted/added to avoid multiple arrows to the same course
                        if prereq not in visited: 
                            visited.add(prereq)
                            course_queue.append(prereq)

                    # Adding equivalent prereqs to graph
                    add_eq_prereqs(graph, get_eq_prereqs(course_value), course, degree_program=graph_degree_program)
                    
                    # add previously unvisited prerequisites for the current course to the course queue and mark them as visited
                    for group in get_eq_prereqs(course_value):
                        for prereq in group:
                            if prereq not in visited: # only add courses that haven't been visted/added to avoid multiple arrows to the same course
                                visited.add(prereq)
                                course_queue.append(prereq)


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

    # does user want a custom file name?
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
    
    # if there is a *, name is likely a department code, and we can get the course attr
    course_attr = name
    if '*' in name:
        course_attr = get_course_attr(name)

    # check if the course attr is a department or a degree
    search_bool = course_attr not in course_data['courses'].keys() and course_attr not in course_data['programs'].keys()

    if search_bool:
        print(name + ' not found.')
        return True

    print("making graph...")
    course_graph = create_course_graph("graph1")
    
    # if the length of name is 4, the graph is for a specific course
    if len(name) > 4 and "*" in name:
        # Creating a graph for a specific course (ex: CIS*3760)
        course_graph.attr(
            label=f'Prerequisite Graph for {name.upper()}',
            labelloc='t',
            fontsize='30'
        )
        parse_prereqs(course_graph, name, course_data, org_name=course_attr)
    else:
        # otherwise, figure out whether to graph a degree or a department
        degree_search = False

        # if the course attr is both,  ask user
        if name in course_data["programs"] and name in course_data["courses"]:
            degree_search = bool_query_loop("\nSeach found in both programs & departments? [program/department] ", "[p/d]", ["program", "p"], ["department", "d"])
        elif name in course_data["programs"]:
            # if course attr is only a degree, search degrees
            degree_search = True

        org_name = name
        # Creating a graph for an entire department (ex: CIS, MATH, ACCT, etc)
        
        if degree_search:
            graph_degree_program(course_graph, name, course_data)
        else:
            # if degree search is false, the course attr must correspond with a department
            course_graph.attr(
                label=f'Prerequisite Graph for all {name.upper()} Courses',
                labelloc='t',
                fontsize='30'
            )
            parse_department(course_graph, name, course_data, org_name)

    # save the graph
    save_graph_to_pdf(course_graph, get_filename(name))
    
    #return whether or not to make another graph
    return bool_query_loop("\nGraph another course? [y/n] ", "[y/n]", ["yes", "y"], ["no", "n"])