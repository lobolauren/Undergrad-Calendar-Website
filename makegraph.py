import json
from posixpath import split
from tkinter.tix import Tree
import graphviz

COLORS = ['blue', 'orange', 'red', 'purple', 'yellow']

# Makegraph helper functions
def saveGraphToPDF(graph, file_name):
    graph.format = 'pdf'
    graph.render(filename=file_name, directory="graph-output").replace('\\', '/')
    # opens graph in PDF viewer
    # graph.view()

# Since we are dealing with pre-requsites, we want a directed graph (one-way)
# So, we'll use a Digraph
def createCourseGraph(filename):
    graph = graphviz.Digraph(filename)
    makeLegend(graph)
    return graph

# Make the Legend for the grapgh
def makeLegend(graph):
    with graph.subgraph(name='clusterLegend') as node:
        node.attr(color="black")
        node.attr(label="Legend")
    
        addOutsideDepartmentCourse(node, "Course Outside of Department")
        addRegularCourse(node, "Normal Prerequisite Course")
        node.edge("Course Outside of Department", "Normal Prerequisite Course")
        show_prereq(node, "Mandatory Prerequisite Course", "Course")
        show_prereq(node, "One of - Prerequisite Course", "Course", color=COLORS[3])
        show_prereq(node, "One of - Prerequisite Course", "Course", color=COLORS[0])
        show_prereq(node, "One of - Prerequisite Course", "Course", color=COLORS[1])
        show_prereq(node, "One of - Prerequisite Course", "Course", color=COLORS[2])


# Change colour of node when course is outside requested department
def addOutsideDepartmentCourse(graph, outsideCourse):
    graph.node(outsideCourse, color="red")


def addRegularCourse(graph, course):
    graph.node(course)


def show_prereq(graph, required_course, child_course, color='green'):
    graph.edge(required_course, child_course, color=color)


def add_eq_prereqs(graph, eq_prereqs, course):

    course_attr = course[:course.index('*')].lower()

    for i, group in enumerate(eq_prereqs):
        for prereq in group:
            
            dep = prereq[:prereq.index('*')].lower()

            # if course not in department, make red
            if dep != course_attr:
                addOutsideDepartmentCourse(graph, prereq)

            show_prereq(graph, prereq, course, color=COLORS[i % len(COLORS)])
            

def parsingPrereq(graph, code, data):

    print("checking prerequisites...")
    course_attr = code[:code.index('*')].lower()
    prereq_list = []

    for course_value in data["courses"][course_attr]:
        if course_value["code"] == code.upper():
            for prereq_value in course_value["prereqs"]["reg_prereqs"]:
                    prereq_list.append(prereq_value)

            add_eq_prereqs(graph, course_value['prereqs']['eq_prereqs'], course_value['code'])

    for prereq in prereq_list:

        dep = prereq[:prereq.index('*')].lower()

        # if course not in department, make red
        if dep != course_attr:
            addOutsideDepartmentCourse(graph, prereq)
        
        show_prereq(graph, prereq, course_value["code"])

        parsingPrereq(graph, prereq,data)


def parsingDepartment(graph, code,data):

    print("checking department...")
    for course_value in data["courses"][code]:
        addRegularCourse(graph,course_value["code"])
        
        add_eq_prereqs(graph, course_value['prereqs']['eq_prereqs'], course_value['code'])

        for prereq in course_value["prereqs"]["reg_prereqs"]:

            dep = prereq[:prereq.index('*')].lower()

            # if course not in department, make red
            if dep != code:
                addOutsideDepartmentCourse(graph, prereq)
            show_prereq(graph,prereq,course_value["code"])


def makegraph(course_data):

    name = input("Course name or department [q to quit]: ").strip().lower()
    
    # allow user to quit
    if name.lower() == 'q' or name.lower() == 'quit':
        return False

    # make sure name is in the data
    try:
        course_attr = name
        # only get this if the input is a full course name
        if '*' in name:
            course_attr = name[:name.index('*')]

        course_data['courses'][course_attr]
    except KeyError:
        print(name + ' not found...')
        return True

    courseGraph = createCourseGraph("graph1")
    print("making graph...")


    if len(name) > 4:
        parsingPrereq(courseGraph, name, course_data)
    else:
        parsingDepartment(courseGraph, name,course_data)

    # file naming
    # remove special characters
    file_name = name+"-graph"
    file_name_query = input("Name graph file? [y/n]: ")
    
    if file_name_query.lower() == "y" or file_name_query.lower() == "yes":
        file_name_input = input("Enter graph name: ")

    # characters not allowed in file names  (windows,linux,mac)
    file_name.replace('*', '')
    file_name.replace('/', '')
    file_name.replace('\\', '')
    file_name.replace(':', '')
    file_name.replace('\"', '')
    file_name.replace('<', '')
    file_name.replace('>', '')
    file_name.replace('|', '')
    file_name.replace('?', '')

    saveGraphToPDF(courseGraph, file_name)

    # Course code (ex. CIS*1300 or CIS or 1300)
    inputFlag = True
    while inputFlag:

        continueSearch = input("\n Graph another course? [y/n] ")

        if continueSearch.lower() == "n" or continueSearch.lower() == "no":
            return False
        return True
