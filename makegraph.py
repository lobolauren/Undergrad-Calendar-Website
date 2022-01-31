import graphviz
from helpers import get_course_attr

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


# Connecting prereq courses on graph
def add_prereq(graph:graphviz.Digraph, required_course, child_course, color='green'):
    graph.edge(required_course, child_course, color=color)


# Adding equivalent prereqs
def add_eq_prereqs(graph:graphviz.Digraph, eq_prereqs, course, org_name):

    course_attr = get_course_attr(course)
    for i, group in enumerate(eq_prereqs):
        for prereq in group:
            if org_name not in prereq.lower(): # if the course if not in the target course's department
                add_outside_department_course(graph, prereq)

            add_prereq(graph, prereq, course, color=COLORS[i % len(COLORS)])
            

# Make the Legend for the graph
def make_legend(graph: graphviz.Digraph):
    with graph.subgraph(name='clusterLegend') as legend:
        legend.attr(color="black")
        legend.attr(label="Legend")
    
        add_outside_department_course(legend, "Course Outside of Department")
        add_regular_course(legend, "Course in Department")
        add_prereq(legend, "Course Outside of Department", "Course in Department", color='black')

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
    while q:
        for _ in range(len(q)):
            course = q.pop(0)
            course_attr = get_course_attr(course)

            for course_value in data['courses'][course_attr]:
                if course_value['code'] == course:

                    # Adding prereqs to graph
                    for prereq in course_value['prereqs']['reg_prereqs']:
                        dep = get_course_attr(prereq)
                        if dep != org_name:  # make red - outside course
                            add_outside_department_course(graph, prereq)
                        add_prereq(graph, prereq, course_value['code'])
                        if prereq not in visited: # only add courses that haven't been visted/added to avoid multiple arrows to the same course
                            visited.add(prereq)
                            q.append(prereq)

                    # Adding equivalent prereqs to graph
                    add_eq_prereqs(graph, course_value['prereqs']['eq_prereqs'], course, org_name)
                    for group in course_value['prereqs']['eq_prereqs']:
                        for prereq in group:
                            if prereq not in visited: # only add courses that haven't been visted/added to avoid multiple arrows to the same course
                                visited.add(prereq)
                                q.append(prereq)


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

    # check for vaid department
    if course_attr not in course_data['courses'].keys():
        print(name + ' not found.')
        return True

    print("making graph...")
    course_graph = create_course_graph("graph1")
    
    if len(name) > 4:
        # Creating a graph for a specific course (ex: CIS*3760)
        course_graph.attr(
            label=f'Prerequisite Graph for {name.upper()}',
            labelloc='t',
            fontsize='30'
        )
        parse_prereqs(course_graph, name, course_data, org_name=course_attr)
    else:
        # Creating a graph for an entire department (ex: CIS, MATH, ACCT, etc)
        org_name = name
        course_graph.attr(
            label=f'Prerequisite Graph for all {name.upper()} Courses',
            labelloc='t',
            fontsize='30'
        )
        parse_department(course_graph, name, course_data, org_name)

    save_graph_to_pdf(course_graph, get_filename(name))

    continue_search = input("\nGraph another course? [y/n] ").strip().lower()
    if continue_search == "n" or continue_search == "no":
        return False
    return True
