from helpers import *
from course_search import get_course_data
import json

DEBUG = False

def add_node(nodes: list, course_code: str, x, y):
    course_code = course_code.lower()
    nodes.append({
        'id': course_code.replace('*', ''),
        'type': 'default',
        'data': {
            'label': course_code.upper().replace('*', ' ')
        },
        'position': {'x': x, 'y': y},
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
        'animated': animated
    })

def make_course_graph(code):

    data = get_course_data()

    nodes = []
    nodes_data = {}
    edges = []

    if not valid_code(code):
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
        for j, value in enumerate(row):
            add_node(nodes, value, j*200 - ((len(row)-1)*200*0.5), i*200)

    return {
        'nodes': nodes,
        'edges': edges
    }
