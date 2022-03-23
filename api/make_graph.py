from helpers import *
from course_search import get_course_data
import json

DEBUG = False

NODE_COLORS = {
    'searched_course': '#ffc107',   # main course
    'same_dept': '#0d6efd',         # course in the same department
    'diff_dept': '#6c757d'          # course in different department
}

def add_node(nodes: list, course_code: str, color):
    course_code = course_code.lower()
    nodes.append({
        'id': course_code.replace('*', ''),
        'data': {
            'label': make_code_valid(course_code).upper().replace('*', ' ')
        },
        'targetPosition': 'left',
        'sourcePosition': 'right',
        'connectable': False,
        'draggable': False,
        'style': {
            'background': color,
        },
    })

def add_edge(edges: list, course: str, prereq: str, animated: bool=False):
    course = course.lower().replace('*', '')
    prereq = prereq.lower().replace('*', '')
    edges.append({
        'id': f'{course}-{prereq}',
        'source': course,
        'target': prereq,
        'animated': animated,
        'markerEnd': {
            'type': 'arrowclosed'
        }
    })

def get_node_color(code, og_dept, og_code):
    if make_code_valid(code) == og_code.upper():
        return NODE_COLORS['searched_course']
    elif get_course_attr(make_code_valid(code), upper=True) == og_dept:
        return NODE_COLORS['same_dept']
    else:
        return NODE_COLORS['diff_dept']

def make_course_graph(code):

    data = get_course_data()

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
            add_node(nodes, cur_course_code, color)

            for prereq in get_reg_prereqs(cur_course):
                if get_course_attr(prereq) not in data['courses']:
                    continue

                add_edge(edges, cur_course_code, prereq)

                if prereq not in visited:
                    visited.add(prereq)
                    q.append(prereq)

            for group in get_eq_prereqs(cur_course):
                for prereq in group:
                    if get_course_attr(prereq) not in data['courses']:
                        continue
                    
                    add_edge(edges, cur_course_code, prereq, animated=True)

                    if prereq not in visited:
                        visited.add(prereq)
                        q.append(prereq)

    return {
        'nodes': nodes,
        'edges': edges
    }


def make_department_graph(department):

    data = get_course_data()

    nodes = []
    edges = []

    for course_value in data["courses"][department]:
        cur_course_code = course_value["code"]
        cur_course = get_course(data, cur_course_code)
        color = get_node_color(cur_course_code, department, cur_course_code)
        add_node(nodes, cur_course_code, color)

        # go through mandatory prereqs
        for prereq in get_reg_prereqs(course_value):
            if prereq == []:
                continue

            add_edge(edges, cur_course_code, prereq, animated=False)

            # Change colour for courses outside department
            if(get_course_attr(prereq, upper=True) != department.upper()):
                color = get_node_color(prereq, department, cur_course_code)
            add_node(nodes, prereq, color)
            
        # go through the other cases for pre-reqs
        for eq_prereq in get_eq_prereqs(course_value):
            if eq_prereq == []:
                continue

            # iterate through each array in eq_prereq
            for course in eq_prereq:
                add_edge(edges, cur_course_code, course, animated=True)   
                # Change colour for courses outside department
                if(get_course_attr(course, upper=True) != department.upper()):
                    color = get_node_color(course, department, cur_course_code)
                add_node(nodes, course, color)               

    return {
        'nodes': nodes,
        'edges': edges
    }

def make_major_program_graph(program):
    data = get_course_data()

    nodes = []
    edges = []

    dept = get_course_attr(program).upper()
    all_courses = data["programs"][program]

    major_courses = all_courses["major_reqs"]
    minor_courses = all_courses["minor_reqs"]
    required_courses = major_courses
    visited = set()
    q = required_courses

    print(q)
    while q:
        cur_course_code = q.pop(0)
        cur_course = get_course(data, cur_course_code)
        color = get_node_color(cur_course_code, dept, program)
        add_node(nodes, cur_course_code, color)
        for prereq in get_reg_prereqs(cur_course):
                if get_course_attr(prereq) not in data['courses']:
                    continue

                add_edge(edges, cur_course_code, prereq)

                if prereq not in visited:
                    visited.add(prereq)
                    q.append(prereq)
        for group in get_eq_prereqs(cur_course):
            for prereq in group:
                if get_course_attr(prereq) not in data['courses']:
                    continue

                add_edge(edges, cur_course_code, prereq, animated=True)

                if prereq not in visited:
                    visited.add(prereq)
                    q.append(prereq)
    print(q)
    print(nodes)
    print(edges)
    return {
        'nodes': nodes,
        'edges': edges
    }

def make_minor_program_graph(program):
    data = get_course_data()

    nodes = []
    edges = []

    dept = get_course_attr(program).upper()
    all_courses = data["programs"][program]

    major_courses = all_courses["major_reqs"]
    minor_courses = all_courses["minor_reqs"]
    required_courses = minor_courses
    visited = set()
    q = required_courses

    print(q)
    while q:
        cur_course_code = q.pop(0)
        cur_course = get_course(data, cur_course_code)
        color = get_node_color(cur_course_code, dept, program)
        add_node(nodes, cur_course_code, color)
        for prereq in get_reg_prereqs(cur_course):
                if get_course_attr(prereq) not in data['courses']:
                    continue

                add_edge(edges, cur_course_code, prereq)

                if prereq not in visited:
                    visited.add(prereq)
                    q.append(prereq)
        for group in get_eq_prereqs(cur_course):
            for prereq in group:
                if get_course_attr(prereq) not in data['courses']:
                    continue

                add_edge(edges, cur_course_code, prereq, animated=True)

                if prereq not in visited:
                    visited.add(prereq)
                    q.append(prereq)
    print(q)
    print(nodes)
    print(edges)
    return {
        'nodes': nodes,
        'edges': edges
    }