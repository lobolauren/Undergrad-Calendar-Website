import json
import time

from typing import List
from playwright.sync_api import sync_playwright, Page


# scrapes page for all course codes (ex. CIS, MATH, AGGR)
def get_course_codes():

    codes_list = []
    # start playwright
    with sync_playwright() as pw:

        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto('https://calendar.carleton.ca/undergrad/courses/')

        # select part of page containing links to course codes
        codes_region = page.query_selector('.tab_content')
        # ignore first 27 because they are just letters of the alphabet for navigation
        codes = codes_region.query_selector_all('a')[:-2]

        # codes are formatted as such: ex. Chemistry (CHEM), we want just CHEM
        for code in codes:
            code_str = code.inner_text()

            # finds index of first bracket, grabs string between that index and the last character
            if '(' in code_str or ')' in code_str:
                # someoneput a bracket in a hyperlink
                code_str = (code_str.replace(')', '')).replace('(', '')
            
            codes_list.append(code_str.lower())
            

        browser.close()

    return codes_list

# remove all commas from between brackets in a string
# ex: "(,,),(,),,(,,,),[,(,,)](,,),,," -> "(),(),,(),[()](),,,"


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
        'eq_prereqs': []  # list of lists each sublist represents related prerequisites
    }

    if prereqs_el:
        prereq_text = prereqs_el.inner_text()

        # the reason we do this is because we noticed that every block of related prerequisites is contained within
        # brackets that are seperated by commas. We then remove the commas from between the brackets so we can seperate
        # each block of related prerequisites by splitting on the comma character
        prereq_text = remove_commas_between_brackets(prereq_text)
        tokens = prereq_text.split(',')

        # we now only want to look at courses that are in a block of related prerequisites so we get all the blocks that
        # contain the bracket characters
        def ftr(s): return True if '(' in s or '[' in s else False
        filtered_tokens = list(filter(ftr, tokens))

        # there there aren't any blocks that in the filtered list then check if the prerequisite text contains the words
        # 'or' or 'of' and if there is add them
        if not filtered_tokens and ('or' in prereq_text or 'of' in prereq_text):
            # if there is only one prerequisite add it to regular prerequisites otherwise add them as related prerequisites
            if len(prereqs_list) < 2:
                prereqs['reg_prereqs'].extend(prereqs_list)
            else:
                prereqs['eq_prereqs'] = [prereqs_list]

        else:
            # copy list because we are going to be removing elements from it while looping through it
            prereqs_list_copy = prereqs_list[:]

            # for each block of related prerequisites, go through and remove any course from the that exists in the block
            # from the original prerequisites list
            for t in filtered_tokens:

                eq_prereqs = []
                for course in prereqs_list:
                    # if the course itself exists in its prerequisties string, remove it and do nothing
                    if course == course_code:
                        prereqs_list_copy.remove(course)
                    # if a course is in the string but appears after the word 'excluding', remove it and do nothing
                    elif 'excluding' in t and course in t[t.index('excluding'):]:
                        prereqs_list_copy.remove(course)
                    # if it finds a course remove it and add it to the temporary list of related prerequisites
                    elif course in t:
                        eq_prereqs.append(course)
                        if course in prereqs_list_copy:
                            prereqs_list_copy.remove(course)

                # if the block only had one prerequisite, make it a regular prerequisite, otherwise add the related prerequisites
                if len(eq_prereqs) > 1:
                    prereqs['eq_prereqs'].append(eq_prereqs)
                else:
                    prereqs_list_copy.extend(eq_prereqs)

            # at this point any prerequisites left in the list are not related and must be required
            prereqs['reg_prereqs'] = prereqs_list_copy

    return prereqs


# finds an element and returns its inner text
def get_element_text(parent_el, query):
    child_el = parent_el.query_selector(query)
    # if there is no text, return an empty string
    return child_el.inner_text() if child_el else ''

# takes a substring and finds the first number in it (assumed to be the course weight)
def extract_weight(weight_str=""):
    weight = "0"
    # get rid of brackets then split
    s_str = weight_str.split(" ")
    # find numeric digit
    for s in s_str:
        if '[' in s:
            s = s.replace('[', '') 
            if s.replace('.', '').isdigit():
                weight = s

    return weight

def extract_title_info(title_str=""):

    obj = {
        'title': '',
        'weight': ''
    }

    # \n seperates the weight/code and title
    li_str = title_str.split("\n")
    
    obj['title'] = li_str[1]
    obj['weight'] = extract_weight(li_str[0])

    return obj
    

# get individual course details from course object
def get_course_details(course):

    # get text for each element
    
    # someone put hex codes in the names
    course_code = get_element_text(course, '.courseblockcode').replace(' ', '*').replace('\u00a0', '*')
    # NOTE: Strange hex numbers all over the place

    course_title_text = get_element_text(course, '.courseblocktitle ')
    course_title_all = extract_title_info(course_title_text)
    course_title = course_title_all['title']
    course_weight = float(course_title_all['weight'])

    # NOTE: still need to get this
    course_desc = ''

    # for formatting, still have these but empty
    course_restrictions = ''
    course_department = ''
    course_location = ''
    course_corequisites = ''
    de_offering = False

    course_terms = []

    # NOTE: need to get prereqs
    # course_prereqs_el = course.query_selector('.detail-prerequisite_s_ span')
    # # get all prerequisite links and add their text to a list
    # course_prereqs_a = course_prereqs_el.query_selector_all(
    #     'a') if course_prereqs_el else []
    # prereqs_a_text = [req.inner_text() for req in course_prereqs_a]
    # prereqs = get_prereqs(course_prereqs_el, prereqs_a_text, course_code)

    prereqs = []

    return {
        'code': course_code.upper(),
        'name': course_title,
        'terms': course_terms,
        'weight': course_weight,
        'description': course_desc,
        'prereqs': prereqs,
        'de': de_offering,
        'restrictions': course_restrictions,
        'department': course_department,
        'location': course_location,
        'coreqs': course_corequisites
    }


# scrape course information from the university website
def get_course_info(course_codes: List[str]):

    course_info = {}
    # playwright startup
    with sync_playwright() as pw:

        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()

        for code in course_codes:

            course_info[code] = []
            if code == 'iaef':  # edge case since the url for the course descriptions is wrong
                page.goto(
                    f'https://calendar.carleton.ca/undergrad/courses/DBST/')
            else:
                page.goto(
                    f'https://calendar.carleton.ca/undergrad/courses/{code.upper()}/')

            print("  Scraping \'"+code+"\' courses...", end='', flush=True)
            # select every course on the page, loop through and get details
            courses = page.query_selector_all('.courseblock')
            for course in courses:
                course_info[code].append(get_course_details(course))

            print(" Done")

        browser.close()

    return course_info


# save dictionary object to a JSON file
def save_dict_as_json(dict, filename):
    with open(filename, 'w') as fp:
        json.dump(dict, fp, indent=4)


def main():
    # set variables to measure time
    debug = True
    start = time.time()

    print("Scraping department codes...", end='', flush=True)
    codes = get_course_codes()
    
    print(" Done")

    print("Scraping course info")
    course_info = get_course_info(codes)

    data = {
        "programs": [],
        "courses": course_info
    }

    print("Saving file...")
    save_dict_as_json(data, filename='course_info_carleton.json')

    end = time.time()
    if debug:
        print(f"Done in {int(end - start)}s.")


if __name__ == '__main__':
    main()
