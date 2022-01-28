import json
import graphviz

COLORS = ['blue', 'yellow', 'red', 'purple', 'orange']

# Makegraph helper functions
def saveGraphToPDF(graph):
    graph.format = 'pdf'
    graph.render(directory="graph-output").replace('\\', '/')
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
        show_prereq(node, "One of these Prerequisite Course", "Course")
        show_prereq(node, "One of these Prerequisite Course", "Course", color=COLORS[0])
        show_prereq(node, "One of these Prerequisite Course", "Course", color=COLORS[1])
        show_prereq(node, "One of these Prerequisite Course", "Course", color=COLORS[2])


# Change colour of node when course is outside requested department
def addOutsideDepartmentCourse(graph, outsideCourse):
    graph.node(outsideCourse, color="red")


def addRegularCourse(graph, course):
    graph.node(course)


def show_prereq(graph, required_course, child_course, color='green'):
    graph.edge(required_course, child_course, color=color)


def add_eq_prereqs(graph, eq_prereqs, course):
    for i, group in enumerate(eq_prereqs):
        for prereq in group:
            show_prereq(graph, prereq, course, color=COLORS[i%len(COLORS)])


def parsingPrereq(code,data,filename):
    course_attr = code[:code.index('*')].lower()
    prereq_list = []
    for course_value in data["courses"][course_attr]:
        if course_value["code"] == code.upper():
            for prereq_value in course_value["prereqs"]["reg_prereqs"]:
                    prereq_list.append(prereq_value)
  #  print("list: "+ str(prereq_list))
    for prereqs in prereq_list:
        show_prereq(filename, prereqs, code.upper())
        parsingPrereq(prereqs,data,filename)


def parsingDepartment(code,data,filename):
    for course_value in data["courses"][code]:
        addRegularCourse(filename,course_value["code"])
        for prereq in course_value["prereqs"]["reg_prereqs"]:
            show_prereq(filename,prereq,course_value["code"])
   


def makegraph(course_data):
    name = input("Course name or department: ").strip().lower()
    courseGraph = createCourseGraph("graph1")
    if len(name) > 4:
        parsingPrereq(name,course_data,courseGraph)
    else:
        parsingDepartment(name,course_data,courseGraph)
    saveGraphToPDF(courseGraph)
    # Course code (ex. CIS*1300 or CIS or 1300)
    inputFlag = True
    while inputFlag:
        print("testing function")
        continueSearch = input("\n Graph another course? [y/n] ")
        if continueSearch.lower() == "n" or continueSearch.lower() == "no":
            return False
        return True
