import json
import time

from typing import List
from playwright.sync_api import sync_playwright


# scrapes page for all course codes (ex. CIS, MATH, AGGR)
def get_course_codes():

    codes_list = []

    # Using synchronus playwright
    with sync_playwright() as pw:
        # launch chromium headless
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto('https://calendar.uoguelph.ca/undergraduate-calendar/course-descriptions/')

        # select part of page containing links to course codes
        codes_region = page.query_selector('.az_sitemap')
        codes = codes_region.query_selector_all('li')[27:] #select all lists (ignore first 27, which are letters of the alphabet)
        # for each code in the list of names
        for code in codes: 
            code_str = code.inner_text()
            # extract the code from the text
            code_str_final = code_str[code_str.index('(')+1:-1] # finds index of first bracket, grabs string between that index & the last character
            # add code to the list in lower case (for navigation on the website)
            codes_list.append(code_str_final.lower())

        browser.close()

    return codes_list


def remove_commas_between_brackets(s):
    new_str = ''
    inside_brackets = False
    outer_bracket = ''
    for c in s:
        if c == ')' and outer_bracket == '(':
            inside_brackets = False
        if c == ']' and outer_bracket == '[':
            inside_brackets = False
        if not inside_brackets or (inside_brackets and c != ','):
            new_str += c
        if not inside_brackets and c == '(' or c == '[':
            outer_bracket = c
            inside_brackets = True
    return new_str


def get_prereqs(prereqs_el, prereqs_list, course_code):

    prereqs = {
        'reg_prereqs': [],
        'eq_prereqs': []
    }

    # search list of prereqs to check if in a '1 of' block
    if prereqs_el:
        prereq_text = prereqs_el.inner_text()
        prereq_text = remove_commas_between_brackets(prereq_text)
        tokens = prereq_text.split(',')

        ftr = lambda s: True if '(' in s or '[' in s else False
        filtered_tokens = list(filter(ftr, tokens))

        if not filtered_tokens and ('or' in prereq_text or 'of' in prereq_text):
            if len(prereqs_list) < 2:
                prereqs['reg_prereqs'].extend(prereqs_list)
            else:
                prereqs['eq_prereqs'] = [prereqs_list]

        else: # for each 'block' of prerequisits, check if any codes from the full list are contained in it, if so, add to the eq_prereqs list
            prereqs_list_copy = prereqs_list[:]
            for t in filtered_tokens:
                eq_prereqs = []
                for course in prereqs_list:
                    if course == course_code:
                        prereqs_list_copy.remove(course)
                    elif 'excluding' in t and course in t[t.index('excluding'):]:
                        prereqs_list_copy.remove(course)
                    elif course in t:
                        eq_prereqs.append(course)
                        if course in prereqs_list_copy:
                            prereqs_list_copy.remove(course)

                if len(eq_prereqs) > 1:
                    prereqs['eq_prereqs'].append(eq_prereqs)
                else:
                    prereqs_list_copy.extend(eq_prereqs)

            prereqs['reg_prereqs'] = prereqs_list_copy
    
    return prereqs


# get individual course details from course object
def get_course_details(course):

    course_code_el = course.query_selector('.detail-code')
    course_code = course_code_el.inner_text()

    course_title_el = course.query_selector('.detail-title')
    course_title = course_title_el.inner_text()

    course_availability_el = course.query_selector('.detail-typically_offered')
    course_availability = course_availability_el.inner_text() if course_availability_el else ''
    
    course_terms = []
    if 'fall' in course_availability.lower():
        course_terms.append('F')
    if 'winter' in course_availability.lower():
        course_terms.append('W')
    if 'summer' in course_availability.lower():
        course_terms.append('S')

    course_prereqs_el = course.query_selector('.detail-prerequisite_s_ span') 
    course_prereqs_a = course_prereqs_el.query_selector_all('a') if course_prereqs_el else []

    prereqs_a_text = [req.inner_text() for req in course_prereqs_a]
    prereqs = get_prereqs(course_prereqs_el, prereqs_a_text, course_code)
    
    course_weight_el = course.query_selector('.detail-hours_html')
    course_weight = float(course_weight_el.inner_text()[1:-1])

    course_desc_el = course.query_selector('.courseblockextra')
    course_desc = course_desc_el.inner_text() if course_desc_el else ''

    course_offering_el = course.query_selector('.detail-offering span')
    course_offering = course_offering_el.inner_text() if course_offering_el else ''

    if 'Distance Education' in course_offering:
        de_offering = True
    else:
        de_offering = False

    course_restrictions_el = course.query_selector('.detail-restriction_s_ span')
    course_restrictions = course_restrictions_el.inner_text() if course_restrictions_el else ''

    course_department_el = course.query_selector('.detail-department_s_ span')
    course_department = course_department_el.inner_text() if course_department_el else ''

    course_location_el = course.query_selector('.detail-location_s_ span')
    course_location = course_location_el.inner_text() if course_location_el else ''

    course_corequisites_el = course.query_selector('.detail-co_requisite_s_ span')
    course_corequisites = course_corequisites_el.inner_text() if course_corequisites_el else ''

    return {
        'code': course_code.upper(),
        'name': course_title,
        'terms': course_terms,
        'weight': course_weight,
        'description': course_desc,
        'prereqs': prereqs,
        'offerings': de_offering,
        'restrictions': course_restrictions,
        'department': course_department,
        'location': course_location,
        'coreqs': course_corequisites
    }


# scrape course information from the university website
def get_course_info(course_codes: List[str]):

    course_info = {}

    with sync_playwright() as pw: 

        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()

        for code in course_codes:
            course_info[code] = []
            if code == 'iaef':
                page.goto(f'https://calendar.uoguelph.ca/undergraduate-calendar/course-descriptions/ieaf/')
            else:
                page.goto(f'https://calendar.uoguelph.ca/undergraduate-calendar/course-descriptions/{code}/')

            print("  Scraping \'"+code+"\' courses...", end='', flush=True)

            courses = page.query_selector_all('.courseblock')
            for course in courses:
                course_info[code].append(get_course_details(course))

            print(" Done")

        browser.close()

    return {'courses': course_info}


# https://calendar.uoguelph.ca/undergraduate-calendar/degree-programs/
def get_degree_program_links(page):
    
    page.goto('https://calendar.uoguelph.ca/undergraduate-calendar/degree-programs/')

    list_els = page.query_selector_all('.sitemap li a')

    links = []
    for list_el in list_els:
        relative_link = list_el.get_attribute("href")
        links.append(f'https://calendar.uoguelph.ca{relative_link}')
    
    return links


# ex: https://calendar.uoguelph.ca/undergraduate-calendar/programs-majors-minors/applied-human-nutrition-ahn/#requirementstext
def get_major_requirements():
    pass


# ex: https://calendar.uoguelph.ca/undergraduate-calendar/degree-programs/bachelor-applied-science-basc/#programstext
def get_program_majors():
    pass


def get_program_info():
    course_info = {}

    with sync_playwright() as pw: 

        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()

        program_links = get_degree_program_links(page)

        browser.close()

    return {'courses': course_info}


# save dictionary object to a JSON file
def save_dict_as_json(dict, filename):
    with open(filename, 'w') as fp:
        json.dump(dict, fp, indent=4)


def main():

    debug = True
    start = time.time()

    # print("Scraping department codes...", end='', flush=True)
    # codes = get_course_codes()
    # print(" Done")

    # print("Scraping course info")
    # course_info = get_course_info(codes)

    print("Scraping program info")
    program_info = get_program_info()

    # print("Saving file...")
    # save_dict_as_json(course_info, filename='course_info.json')

    # end = time.time()
    # if debug:
    #     print(f"Done in {int(end - start)}s.")


if __name__ == '__main__':
    main()
