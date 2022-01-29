import graphviz

COLORS = ['blue', 'orange', 'red', 'purple', 'yellow']

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
def add_outside_department_course(graph: graphviz.Digraph, outside_course):
    graph.node(outside_course, color="red")


def add_regular_course(graph: graphviz.Digraph, course):
    graph.node(course)


def add_prereq(graph: graphviz.Digraph, required_course, child_course, color='green'):
    graph.edge(required_course, child_course, color=color)


def add_eq_prereqs(graph: graphviz.Digraph, eq_prereqs, course):

    course_attr = course[:course.index('*')].lower()

    for i, group in enumerate(eq_prereqs):
        for prereq in group:
            if course_attr not in prereq.lower():
                add_outside_department_course(graph, prereq)

            add_prereq(graph, prereq, course, color=COLORS[i % len(COLORS)])


# Make the Legend for the grapgh
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


def parse_prereqs(graph, code, data):

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
        if dep != course_attr:  # make red
            add_outside_department_course(graph, prereq)
        
        add_prereq(graph, prereq, course_value["code"])
        parse_prereqs(graph, prereq, data)


def parse_department(graph: graphviz.Digraph, code, data):

    print("checking department...")
    for course_value in data["courses"][code]:

        add_regular_course(graph, course_value["code"])
        add_eq_prereqs(graph, course_value['prereqs']['eq_prereqs'], course_value['code'])

        for prereq in course_value["prereqs"]["reg_prereqs"]:
            dep = prereq[:prereq.index('*')].lower()
            if dep != code: # make red
                add_outside_department_course(graph, prereq)
            add_prereq(graph,prereq,course_value["code"])


# remove characters that aren't allowed in a filename
def fix_filename(filename):
    bad_chars = ['*', '/', '\\', ':', '\"', '<', '>', '|', '?']
    for c in bad_chars:
        filename = filename.replace(c, '')
    return filename


def get_filename(name):
    filename = name+"-graph"
    filename_query = input("Name graph file? [y/n]: ").strip().lower()

    if filename_query == "y" or filename_query == "yes":
        filename = input("Enter graph name: ").strip()

    filename = fix_filename(filename)
    return filename


def makegraph(course_data):

    name = input("Course name or department [q to quit]: ").strip().lower()
    
    # allow user to quit
    if name.lower() == 'q' or name.lower() == 'quit':
        return False
    
    course_attr = name
    if '*' in name:
        course_attr = name[:name.index('*')]

    # check for vaid department
    if course_attr not in course_data['courses'].keys():
        print(name + ' not found.')
        return True

    print("making graph...")
    course_graph = create_course_graph("graph1")

    if len(name) > 4:
        parse_prereqs(course_graph, name, course_data)
    else:
        parse_department(course_graph, name, course_data)

    save_graph_to_pdf(course_graph, get_filename(name))

    continue_search = input("\nGraph another course? [y/n] ").strip().lower()
    if continue_search == "n" or continue_search == "no":
        return False
    return True
