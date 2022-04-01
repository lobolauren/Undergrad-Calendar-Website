from helpers import *
from course_search import get_course_data, COURSE_INFO_JSON
import json

DEBUG = False

NODE_COLORS = {
    'searched_course': 'warning',   # main course
    'same_dept': 'primary',         # course in the same department
    'diff_dept': 'secondary'          # course in different department
}

default_node_textsize = 14.0
legend_node_textsize = 10.0
COLORS = ['blue', 'orange', 'red', 'purple', 'yellow']


def add_node(nodes: list, course_code: str, color, course_name='', description='', courseSearched=False):
    course_code = course_code.lower()
    nodes.append({
        'id': course_code.replace('*', ''),
        'data': {
            'id': course_code.replace('*', ''),
            'label': make_code_valid(course_code).upper().replace('*', ' '),
            'code': course_code,
            'color': color,
            'description': description,
            'name': course_name,
            'courseSearched': courseSearched,
            'dropValue': 0,
            # 'dropped': False
        },
        'type': 'courseNode',
        'targetPosition': 'left',
        'sourcePosition': 'right',
        'connectable': False,
        'draggable': False,
    })

def add_edge(edges: list, course: str, prereq: str, color,animated: bool=False):
    course = course.lower().replace('*', '')
    prereq = prereq.lower().replace('*', '')
    edges.append({
        'id': f'{course}-{prereq}',
        'source': course,
        'target': prereq, 
        'animated': animated,
        'style': {
            'stroke': color,
        },
        'markerEnd': {
            'type': 'arrowclosed'
        },
    })

def get_node_color(code, og_dept, og_code):
    if make_code_valid(code) == og_code.upper():
        return NODE_COLORS['searched_course']
    elif get_course_attr(make_code_valid(code), upper=True) == og_dept:
        return NODE_COLORS['same_dept']
    else:
        return NODE_COLORS['diff_dept']

# makes a graph of a course
def make_course_graph(code, school: str = COURSE_INFO_JSON):

    # get the correct file name
    if school == 'guelph':
        school = COURSE_INFO_JSON
    elif school == 'carleton':
        school = 'course_info_carleton.json'

    data = get_course_data(school)
    
    nodes = []
    edges = []

    if not get_course(data, code):
        return {
            'nodes': nodes,
            'edges': edges
        }

    dept = get_course_attr(code).upper()

    visited = set()
    q = [code.upper()]

    while q:
        for _ in range(len(q)):
            cur_course_code = q.pop(0)

            if get_course_attr(cur_course_code) not in data['courses']:
                continue

            cur_course = get_course(data, cur_course_code)
            color = get_node_color(cur_course_code, dept, code)
            add_node(nodes, cur_course_code, color, cur_course['name'], cur_course['description'], courseSearched=True)

            for prereq in get_reg_prereqs(cur_course):
                if get_course_attr(prereq) not in data['courses']:
                    continue

                add_edge(edges, cur_course_code, prereq,color='green')

                if prereq not in visited:
                    visited.add(prereq)
                    q.append(prereq)

            for i, group in enumerate(get_eq_prereqs(cur_course)):
                for prereq in group:
                    if get_course_attr(prereq) not in data['courses']:
                        continue
                    add_edge(edges, cur_course_code, prereq, color=COLORS[i % len(COLORS)],animated=True)

                    if prereq not in visited:
                        visited.add(prereq)
                        q.append(prereq)

    return {
        'nodes': nodes,
        'edges': edges
    }


def make_department_graph(department, school: str = COURSE_INFO_JSON):

    # get the correct file name
    if school == 'guelph':
        school = COURSE_INFO_JSON
    elif school == 'carleton':
        school = 'course_info_carleton.json'


    data = get_course_data(school)

    nodes = []
    edges = []
    visited = set()

    for course_value in data["courses"][department]:
        # get the current course and add the course node with the correct colour
        cur_course_code = course_value["code"]
        color = get_node_color(cur_course_code, department.upper(), department.upper())
        if cur_course_code not in visited:
            visited.add(cur_course_code)
            add_node(nodes, cur_course_code, color, course_value['name'], course_value['description'])
        

        for prereq in get_reg_prereqs(course_value):
            if prereq == []:
                continue

            add_edge(edges, cur_course_code, prereq, color='green', animated=False)
            # Change colour for courses outside department
            color = get_node_color(prereq, department.upper(), cur_course_code)

            if prereq not in visited:
                visited.add(prereq)
                if "*" in prereq:
                    course_code = get_course(data, prereq)
                    add_node(nodes, prereq, color, course_code['name'], course_code['description']) 
                else:
                    add_node(nodes, prereq, color) 
            

            
        # go through the other cases for pre-reqs
        for i,eq_prereq in enumerate(get_eq_prereqs(course_value)):
            if eq_prereq == []:
                continue

            # iterate through each array in eq_prereq
            for course in eq_prereq:
                add_edge(edges, cur_course_code, course,color=COLORS[i % len(COLORS)], animated=True)   
                # Change colour for courses outside department
                color = get_node_color(course, department.upper(), cur_course_code)

                if course not in visited:
                    visited.add(prereq)
                    if "*" in prereq:
                        course_code = get_course(data, course)
                        add_node(nodes, course, color, course_code['name'], course_code['description'])    
                    else:
                        add_node(nodes, prereq, color)        
    
    return {
        'nodes': nodes,
        'edges': edges
    }


def make_major_program_graph(program, school: str = COURSE_INFO_JSON):
    data = get_course_data(school)

    nodes = []
    edges = []

    
    all_courses = data["programs"][program]

    major_courses = all_courses["major_reqs"]
    required_courses = major_courses
    visited = set()
    q = required_courses

    if(program.upper() == "CS"):
        dept = get_course_attr(q[0]).upper()
    else:
        dept = get_course_attr(program).upper()
    
    while q:
        cur_course_code = q.pop(0)
        cur_course = get_course(data, cur_course_code)
        color = get_node_color(cur_course_code, dept, program)
        add_node(nodes, cur_course_code, color, cur_course['name'], cur_course['description'])
        for prereq in get_reg_prereqs(cur_course):
                if get_course_attr(prereq) not in data['courses']:
                    continue

                add_edge(edges, cur_course_code, prereq,color='green')

                if prereq not in visited:
                    visited.add(prereq)
                    q.append(prereq)
        for i,group in enumerate(get_eq_prereqs(cur_course)):
            for prereq in group:
                if get_course_attr(prereq) not in data['courses']:
                    continue
                add_edge(edges, cur_course_code, prereq, color=COLORS[i % len(COLORS)],animated=True)

                if prereq not in visited:
                    visited.add(prereq)
                    q.append(prereq)
    return {
        'nodes': nodes,
        'edges': edges
    }


def make_minor_program_graph(program, school: str = COURSE_INFO_JSON):
    data = get_course_data(school)

    nodes = []
    edges = []

    dept = get_course_attr(program).upper()
    all_courses = data["programs"][program]

    minor_courses = all_courses["minor_reqs"]
    required_courses = minor_courses
    visited = set()
    q = required_courses

    while q:
        cur_course_code = q.pop(0)
        cur_course = get_course(data, cur_course_code)
        color = get_node_color(cur_course_code, dept, program)
        add_node(nodes, cur_course_code, color, cur_course['name'], cur_course['description'])
        for prereq in get_reg_prereqs(cur_course):
                if get_course_attr(prereq) not in data['courses']:
                    continue

                add_edge(edges, cur_course_code, prereq,color='green')

                if prereq not in visited:
                    visited.add(prereq)
                    q.append(prereq)
        for i,group in enumerate(get_eq_prereqs(cur_course)):
            for prereq in group:
                if get_course_attr(prereq) not in data['courses']:
                    continue
                add_edge(edges, cur_course_code, prereq, color=COLORS[i % len(COLORS)],animated=True)

                if prereq not in visited:
                    visited.add(prereq)
                    q.append(prereq)

    return {
        'nodes': nodes,
        'edges': edges
    }

