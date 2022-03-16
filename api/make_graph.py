from helpers import *
from course_search import get_course_data
import json

DEBUG = False

NODE_COLORS = {
    'searched_course': '#ffc107',
    'same_dept': '#0d6efd',
    'diff_dept': '#6c757d'
}

def add_node(nodes: list, course_code: str, x, y, color):
    course_code = course_code.lower()
    nodes.append({
        'id': course_code.replace('*', ''),
        'data': {
            'label': make_code_valid(course_code).upper().replace('*', ' ')
        },
        'position': {'x': x, 'y': y},
        'targetPosition': 'left',
        'sourcePosition': 'right',
        'connectable': False,
        'draggable': False,
        'style': {
            'background': color,
        },
    })

def update_nodes(nodes_data, course, depth):
    key = course.lower().replace('*', '')
    nodes_data[key] = depth

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
    if make_code_valid(code) == og_code:
        return NODE_COLORS['searched_course']
    elif get_course_attr(make_code_valid(code)) == og_dept:
        return NODE_COLORS['same_dept']
    else:
        return NODE_COLORS['diff_dept']

def make_course_graph(code):

    data = get_course_data()

    nodes = []
    nodes_data = {}
    edges = []

    if not get_course(data, code):
        return {
            'nodes': nodes,
            'edges': edges
        }

    dept = get_course_attr(code)

    visited = set()
    q = [code.upper()]

    depth = 0
    while q:
        depth += 1
        for _ in range(len(q)):
            cur_course_code = q.pop(0)

            if get_course_attr(cur_course_code) not in data['courses']:
                continue

            cur_course = get_course(data, cur_course_code)
            update_nodes(nodes_data, cur_course_code, depth)
            # if DEBUG:
            #     print(f'{cur_course_code} [{depth}, {count}]')

            for prereq in get_reg_prereqs(cur_course):
                if get_course_attr(prereq) not in data['courses']:
                    continue

                add_edge(edges, cur_course_code, prereq)
                # if DEBUG:
                #     print(f'   {cur_course_code} -> {prereq}')

                if prereq not in visited:
                    visited.add(prereq)
                q.append(prereq)

            for group in get_eq_prereqs(cur_course):
                for prereq in group:
                    if get_course_attr(prereq) not in data['courses']:
                        continue
                    
                    add_edge(edges, cur_course_code, prereq, animated=True)
                    # if DEBUG:
                    #     print(f'   {cur_course_code} -> {prereq}')

                    if prereq not in visited:
                        visited.add(prereq)
                    q.append(prereq)

    temp = [[] for _ in range(max(nodes_data.values()))]
    for node, val in nodes_data.items():
        temp[val-1].append(node)

    nodes = []
    for i, row in enumerate(temp):
        for j, course in enumerate(row):
            color = get_node_color(course, dept, code)
            y, x = j*100-((len(row)-1)*100*0.5), i*300
            add_node(nodes, course, x, y, color)

    return {
        'nodes': nodes,
        'edges': edges
    }
