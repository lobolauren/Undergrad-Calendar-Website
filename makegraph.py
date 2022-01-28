import json
from turtle import color
import graphviz

COLORS = ['blue', 'yellow', 'red', 'purple', 'orange']

def makegraph(course_data):
    name = input("Course name or department: ").strip().lower()

    # Course code (ex. CIS*1300 or CIS or 1300)
    inputFlag = True
    while inputFlag:
        print("testing function")
        continueSearch = input("\n Graph another course? [y/n] ")
        if continueSearch.lower() == "n" or continueSearch.lower() == "no":
            return False
        return True

# Makegraph helper functions
def saveGraphToPDF(graph):
    graph.format = 'pdf'
    graph.render(directory="doctest-output").replace('\\', '/')
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
    with graph.subgraph(name='clusterLegend') as c:
        c.attr(color="black")
        c.attr(label="Legend")

        addOutsideDepartmentCourse(c, "Course Outside of Department")
        addRegularCourse(c, "Normal Prerequisite Course")
        c.edge("Course Outside of Department", "Normal Prerequisite Course")
        show_prereq(c, "Mandatory Prerequisite Course", "Course")
        show_prereq(c, "One of these Prerequisite Course", "Course")
        show_prereq(c, "One of these Prerequisite Course", "Course", color=COLORS[0])
        show_prereq(c, "One of these Prerequisite Course", "Course", color=COLORS[1])
        show_prereq(c, "One of these Prerequisite Course", "Course", color=COLORS[2])


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


# Test code
# courseGraph = createCourseGraph("CourseGraph")
# # EX. 1300
# showRequiredPrerequisiteCourse(courseGraph, "CIS*1300", "CIS*2500")
# # EX. 1300
# showRequiredPrerequisiteCourse(courseGraph, "CIS*1300", "CIS*2170")
# # EX. (2500 or 2170), (1 of 1900, 2110, 2750)
# showOptionalPrerequisiteCourse1(courseGraph, "CIS*2500", "CIS*3760")
# showOptionalPrerequisiteCourse1(courseGraph, "CIS*2170", "CIS*3760")
# showOptionalPrerequisiteCourse2(courseGraph, "CIS*1900", "CIS*3760")
# showOptionalPrerequisiteCourse2(courseGraph, "CIS*2110", "CIS*3760")
# showOptionalPrerequisiteCourse2(courseGraph, "CIS*2750", "CIS*3760")
# # EX. 3760
# showRequiredPrerequisiteCourse(courseGraph, "CIS*3760", "CIS*4250")

# saveGraphToPDF(courseGraph)