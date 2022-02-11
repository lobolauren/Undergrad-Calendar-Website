import PyPDF2
import io

from graphviz import Digraph
from helpers import *

COLORS = ['blue', 'orange', 'red', 'purple', 'yellow'] # to help visually organize the graph
DEFAULT_GRAPH_ATTRS = {
    'labelloc': 't',
    'size': '11,4!',
    'ratio': 'fill'
}

# Makegraph helper functions
def save_graph_to_pdf(graph: Digraph, filename, log=False, cleanup=True):
    graph.format = 'pdf'
    f = graph.render(filename=filename, directory="graph-output", cleanup=cleanup).replace('\\', '/')
    print(f'file saved to: {f}')


# add necessary elements to legend
def build_legend(legend: Digraph):
    legend.attr(
        **DEFAULT_GRAPH_ATTRS,
        color="black",
        label="Legend",
        style="filled",
        fillcolor="azure",
    )

    # department/degree exceptions
    # first creates nodes, then connects them with add_prereq
    with legend.subgraph(name='sub1') as sub1:
        add_outside_department_course(sub1, "Course Outside of Department")
        add_regular_course(sub1, "Course in Department")
        add_outside_required_courses(sub1, "Course not required by degree program")
        add_prereq(sub1, "Course Outside of Department", "Course in Department", color='black')
        add_prereq(sub1, "Course not required by degree program", "Course in Department", color='black')

    # prerequisites examples
    with legend.subgraph(name='sub2') as sub2:
        add_prereq(sub2, "Required Prerequisite", "Course")
        add_prereq(sub2, "One of Prerequisite", "Course", color=COLORS[3])
        add_prereq(sub2, "One of Prerequisite", "Course", color=COLORS[0])
        add_prereq(sub2, "One of Prerequisite", "Course", color=COLORS[1])
        add_prereq(sub2, "One of Prerequisite", "Course", color=COLORS[2])


# create a new legend graph
def make_legend() -> Digraph:
    legend = Digraph()
    build_legend(legend)
    return legend


# add legend to existing graph as a subgraph
def add_legend(graph: Digraph):
    with graph.subgraph(name='clusterLegend') as legend:
        build_legend(legend)


# Since we are dealing with pre-requsites, we want a directed graph (one-way)
def create_course_graph(name, include_legend=True):
    graph = Digraph()
    graph.attr('graph', ranksep="2")
    if include_legend:
        add_legend(graph)
    return graph


# Change colour of node when course is outside requested department
#   If a MATH course is a prereq for a CIS course, MATH is an "outside course"
def add_outside_department_course(graph: Digraph, course):
    graph.node(course, color="salmon", style="filled", fillcolor="lightgray", shape="rect")


# Adding target course to graph
def add_regular_course(graph: Digraph, course):
    graph.node(course, style="filled", fillcolor="aliceblue")


# add a course that is not in the same department and is required
def add_outside_required_courses(graph: Digraph, course):
    graph.node(course, color="chocolate4", style="filled", fillcolor="lightgray", shape="rect")


# Connecting prereq courses on graph
def add_prereq(graph: Digraph, prereq, course, color='green'):
    graph.edge(prereq, course, color=color)


# Adding equivalent prereqs
def add_eq_prereqs(graph: Digraph, eq_prereqs, course, org_name="", degree_program=False):

    course_attr = get_course_attr(course)
    for i, group in enumerate(eq_prereqs):
        for prereq in group:
            # if the course if not in the target course's department
            if (not degree_program) and org_name and (org_name not in prereq.lower()):
                add_outside_department_course(graph, prereq)

            add_prereq(graph, prereq, course, color=COLORS[i % len(COLORS)])


# Department is specified when working with parse_prereqs (which graphs for a single course + its prerequsites)
# When graphing a degree program, department is skipped and graph_degree_program + required_courses are passed in
# graph is the graph, course_info is the data structure containing degrees, prerequisistes, etc., visited is a set of courses that have already been added to the graph,
# department is the course_attr for the current department, set graph_degree_programs to true if the graph is for a program, required courses is a list of courses for the degree
def navigate_course_queue(graph: Digraph, course_info, initial_queue, dept="", graph_degree_program=False, required_courses=[]):

    course_queue = initial_queue
    visited = set() # courses already added to the graph

    for req_course in required_courses:
        visited.add(req_course)

    # until the queue is empty
    while course_queue:

        # do this for each course in the course queue
        for _ in range(len(course_queue)):
            # This process adds the popped course to the graph
            course = course_queue.pop(0)
            course_attr = get_course_attr(course)

            # skips the current course if not in the list of courses
            # this applies to all the high school courses that are scrapped
            if (course_attr not in course_info['courses']):
                continue

            # find the course in the list of courses for the department
            for course_value in course_info['courses'][course_attr]:
                if course_value['code'] == course:

                    # if graph is for degree program and the course being added is not required for the degree
                    if graph_degree_program and course not in required_courses:
                        add_outside_required_courses(graph, course) # Colours outside courses brown
                    else:
                        add_regular_course(graph, course) # Coloured as black

                    # add prereqs for the curent course to the graph
                    for prereq in get_reg_prereqs(course_value):
                        # get department code for the prereq
                        prereq_dep = get_course_attr(prereq)
                        
                        # only done for graphing single course
                        if not graph_degree_program and prereq_dep != dept:  # make red - outside course
                            add_outside_department_course(graph, prereq)
                        
                        add_prereq(graph, prereq, course_value['code'])
                        
                        # only add courses that haven't been visted/added to avoid multiple arrows to the same course
                        if prereq not in visited: 
                            visited.add(prereq)
                            course_queue.append(prereq)

                    # Adding equivalent prereqs to graph
                    add_eq_prereqs(graph, get_eq_prereqs(course_value), course, dept, degree_program=graph_degree_program)
                    
                    # add previously unvisited prerequisites for the current course to the course queue and mark them as visited
                    for group in get_eq_prereqs(course_value):
                        for prereq in group:
                            if prereq not in visited: # only add courses that haven't been visted/added to avoid multiple arrows to the same course
                                visited.add(prereq)
                                course_queue.append(prereq)


# Building prereq graph for a target course
def graph_course(graph: Digraph, code, data, org_name, log=True):
    if log:
        print(f"Graphing {code.upper()}...")

    graph.attr(
        **DEFAULT_GRAPH_ATTRS,
        label=f'Prerequisite Graph for {code.upper()}', 
        fontsize='30'
    )
    
    navigate_course_queue(graph, data, initial_queue=[code.upper()], dept=org_name)


# Building a graph for an entire department
def graph_department(graph: Digraph, code, data, org_name, log=True):
    if log:
        print("Graphing Department...")

    graph.attr(
        **DEFAULT_GRAPH_ATTRS,
        label=f'Prerequisite Graph for all {org_name.upper()} Courses', 
        fontsize='30'
    )

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
def graph_degree_program(graph: Digraph, degree_program, course_info, log=True):
    if log:
        print("Graphing Degree Program...")

    #full degree object within programs
    all_courses = course_info["programs"][degree_program.lower()]

    bachelor = all_courses['bachelor']
    title = all_courses['title']

    # add graph title
    graph.attr(label=f'{bachelor}: {title} - major', labelloc='t', fontsize='30')

    # list all major and minor courses
    major_courses = all_courses["major_reqs"]
    minor_courses = all_courses["minor_reqs"]

    # if minor_courses is empty, minor_search is false
    minor_search = minor_courses

    # if both major and minor are found, ask user
    if major_courses and minor_courses:
        minor_search = bool_query_loop("\nSearch for major or minor? [major/minor] ", 
            err_str="[ma/mi]",
            true_res=["minor", "mi"],
            false_res=["major", "ma"])

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

    # adds all the required courses, pre-reqs, and equivalent prereqs into the graph
    navigate_course_queue(graph, course_info, initial_queue=required_courses[:], graph_degree_program=True, required_courses=required_courses)


# Remove characters that aren't allowed in a filename
def fix_filename(filename: str):
    bad_chars = ['*', '/', '\\', ':', '\"', '<', '>', '|', '?']
    for c in bad_chars:
        filename = filename.replace(c, '')
    return filename


# Getting name of file to store graph
def get_filename(name: str):
    filename = name+"-graph"

    if bool_query_loop('Name graph file? [y/n] '):
        filename = input("Enter graph name: ").strip()

    return fix_filename(filename)


# make a multi-page pdf file with each department on a different page
def make_dept_catalog(course_data, filename):
    merger = PyPDF2.PdfFileMerger(strict=True)
    
    legend = make_legend()
    legend_pdf = PyPDF2.PdfFileReader(io.BytesIO(legend.pipe()))
    merger.append(legend_pdf)

    for dept in get_all_depts(course_data):
        dept_graph = Digraph()
        graph_department(dept_graph, dept, course_data, org_name=dept, log=False)

        dept_graph_pdf = PyPDF2.PdfFileReader(io.BytesIO(dept_graph.pipe()))
        merger.append(dept_graph_pdf)

    filename = filename if filename else get_filename('department-catalog')+'.pdf'  
    merger.write(f'graph-output/{filename}')
    print(f'file saved as: {filename}')


def make_course_catalog(course_data, filename):
    merger = PyPDF2.PdfFileMerger(strict=True)
    
    legend = make_legend()
    legend_pdf = PyPDF2.PdfFileReader(io.BytesIO(legend.pipe()))
    merger.append(legend_pdf)

    for course in get_all_courses(course_data):
        course_graph = Digraph()
        graph_course(course_graph, course['code'], course_data, org_name=get_course_attr(course['code']), log=False)

        course_graph_pdf = PyPDF2.PdfFileReader(io.BytesIO(course_graph.pipe()))
        merger.append(course_graph_pdf)

    filename = filename if filename else get_filename('course-catalog')+'.pdf'  
    merger.write(f'graph-output/{filename}')
    print(f'file saved as: {filename}')


# Makes graph given JSON file data
def makegraph(course_data, department, program, course, make_catalog, output_file):

    # if -C argument is given
    if make_catalog:
        print('Making Department Catalog...')
        if output_file and not output_file.endswith('.pdf'):
            output_file += '.pdf'
        make_dept_catalog(course_data, output_file)
        return False

    output_file.replace('.pdf', '')
    course_graph = create_course_graph("graph1")

    if department:
        print('Making Prerequisite Graph...')
        if valid_dept(department, get_all_depts(course_data)):
            graph_department(course_graph, department, course_data, org_name=department)
            save_graph_to_pdf(course_graph, output_file if output_file else get_filename(department))
        else:
            print(f'{department} not found.')
        return False

    if program:
        print('Making Prerequisite Graph...')
        if valid_program(program, get_all_programs(course_data)):
            graph_degree_program(course_graph, program, course_data)
            save_graph_to_pdf(course_graph, output_file if output_file else get_filename(program))
        else:
            print(f'{program} not found.')
        return False

    if course:
        print('Making Prerequisite Graph...')
        if get_course(course_data, course):
            dept = get_course_attr(course)
            graph_course(course_graph, course, course_data, org_name=dept)
            save_graph_to_pdf(course_graph, output_file if output_file else get_filename(course))
        else:
            print(f'{course} not found.')
        return False

    print('\nPrerequisite Graph Maker')
    print('------------------------')

    input_ = input("Course code or department [q to quit]: ").strip().lower()
    if is_quit(input_):
        return False
    
    if get_course(course_data, input_):
        course_code = input_
        dept = get_course_attr(course_code)
        graph_course(course_graph, course_code, course_data, org_name=dept)

    else:
        dept = input_

        if valid_dept(dept, get_all_depts(course_data)) and valid_program(dept, get_all_programs(course_data)):
            # ask if the users wants department or degree
            degree_search = bool_query_loop(
                "\nSeach found in both programs & departments? [program/department] ", 
                err_str="[p/d]", 
                true_res=["program", "p"], 
                false_res=["department", "d"])

            if degree_search:
                graph_degree_program(course_graph, dept, course_data)
            else:
                graph_department(course_graph, dept, course_data, input_)

        elif valid_dept(dept, get_all_depts(course_data)):
            graph_department(course_graph, dept, course_data, input_)

        elif valid_program(dept, get_all_programs(course_data)):
            graph_degree_program(course_graph, dept, course_data)

        else:
            print(f'{dept} not found.')
            return True

    # save the graph
    save_graph_to_pdf(course_graph, output_file if output_file else get_filename(input_))
    
    # return whether or not to make another graph
    return bool_query_loop("\nMake another graph? [y/n] ")
