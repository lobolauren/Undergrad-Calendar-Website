import json
from textwrap import indent
from tkinter import W
from typing import List
from playwright.sync_api import sync_playwright


def get_course_codes():
    codes = []
    with open('course_codes.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            codes.append(line.strip())
    return codes


def get_course_info(course_codes: List[str]):

    course_info = {}

    with sync_playwright() as pw: 

        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()

        for code in course_codes:
            course_info[code.upper()] = []
            page.goto(f'https://calendar.uoguelph.ca/undergraduate-calendar/course-descriptions/{code}/')

            courses = page.query_selector_all('.courseblock')
            for course in courses:
                course_code_el = course.query_selector('.detail-code')
                course_code = course_code_el.inner_text()

                course_title_el = course.query_selector('.detail-title')
                course_title = course_title_el.inner_text()

                course_offerings_el = course.query_selector('.detail-typically_offered')
                course_offerings = course_offerings_el.inner_text() if course_offerings_el else ''

                course_terms = []
                if 'fall' in course_offerings.lower():
                    course_terms.append('F')
                if 'winter' in course_offerings.lower():
                    course_terms.append('W')
                if 'summer' in course_offerings.lower():
                    course_terms.append('S')

                course_weight_el = course.query_selector('.detail-hours_html')
                course_weight = float(course_weight_el.inner_text()[1:-1])

                course_info[code.upper()].append({
                    'code': course_code.upper(),
                    'name': course_title,
                    'terms': course_terms,
                    'weight': course_weight
                })

        browser.close()

    return course_info


def save_dict_as_json(course_info, filename):
    with open(filename, 'w') as fp:
        json.dump(course_info, fp, indent=4)


def main():
    codes = get_course_codes()
    course_info = get_course_info(codes)
    save_dict_as_json(course_info, filename='course_info.json')


if __name__ == '__main__':
    main()
