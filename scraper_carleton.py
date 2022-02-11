import json
from lib2to3.pgen2 import token
import time
import re

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



def get_prereqs(prereqs_el, prereqs_list, course_code):
    
    prereqs = {
        'reg_prereqs': [],
        'eq_prereqs': []  # list of lists each sublist represents related prerequisites
    }
    if prereqs_el:
        prereq_text = prereqs_el.inner_text()
        prereq_text.split("\n")
      
        # the reason we do this is because we noticed that every block of related prerequisites is contained within
        # brackets that are seperated by commas. We then remove the commas from between the brackets so we can seperate
        # each block of related prerequisites by splitting on the comma character
        prereq_text = remove_commas_between_brackets(prereq_text)
        
        # this is done because the extra information for each course which contained the prerequisite list
        # was one massive string we sliced it that it was only the section that had the prerequisite list
        if "Prerequisite(s):" in prereq_text:
            prereq_text = prereq_text.split("Prerequisite(s):",1)[1]
            prereq_text = prereq_text.split(".",1)[0]
        else:
            prereq_text =" "

        prereq_t = prereq_text.replace('Prerequisite(s):','')

        # split the prerequisite string by and since most courses used this method to sparate their list (see read me for special cases)
        tokens = prereq_t.split('and')
        
        for i, n in enumerate(tokens):
            tokens[i]=n.replace('\xa0',' ')

        #A new list is made because the extra description of each course contained hyperlinks that were not actually prerequisites, but rather
        # graduate course equivalents    
        reqlist = []
        for ele in prereqs_list:
            for tolk in tokens:
                if ele in tolk:
                    reqlist.append(ele)

        #list to hold each section of prerequisites separated by AND
        individual_and_prereqs = []

        for elements in tokens:
            #list to hold the individual special cases of or,one of etc
            new_preqs_list  = []

            # courses that contains prereqs with one of...
            if "of" in elements:
                individual_and_prereqs = re.split(',|or|/',elements)

                # check for the course in the reqlist to ensure they are not graduate courses
                for ele in individual_and_prereqs:
                    for tolk in reqlist:
                        if tolk in ele:
                            new_preqs_list.append(tolk)
               # if the length of the list has more than one element add it to eq_prereqs otherwise reg_prereqs
               # this is because some words in the prereq course requirment description contains of or or so the
               # program thinks it is a special case when it is a regular course
                if len(new_preqs_list) > 1: 
                    prereqs['eq_prereqs'].append(new_preqs_list)
                else:
                    for ele in new_preqs_list:
                        prereqs['reg_prereqs'].append(ele)     
            elif "or" in elements:
                individual_and_prereqs = re.split('or|/',elements)

                # check for the course in the reqlist to ensure they are not graduate courses
                for ele in individual_and_prereqs:
                    for tolk in reqlist:
                        if tolk in ele:
                            new_preqs_list.append(tolk)

                # if the length of the list has more than one element add it to eq_prereqs otherwise reg_prereqs
                # this is because some words in the prereq course requirment description contains of or or so the
                # program thinks it is a special case when it is a regular course
                if len(new_preqs_list) > 1: 
                    prereqs['eq_prereqs'].append(new_preqs_list)
                else:
                    for ele in new_preqs_list:
                        prereqs['reg_prereqs'].append(ele)   
               
            else: #for individual regular course requirments
                individual_and_prereqs = re.split(',.',elements)

                #to check once again that the courses are only those in prereqs and not graduate courses
                for course in individual_and_prereqs:
                    for tolk in reqlist:
                        if tolk in course:
                            prereqs['reg_prereqs'].append(tolk)   
   
    return prereqs
    

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

    li_str = course.inner_text().split("\n")
    course_desc = li_str[2]

    # for formatting, still have these but empty
    course_restrictions = ''
    course_department = ''
    course_location = ''
    course_corequisites = ''
    de_offering = False

    course_terms = []

    # NOTE: need to get prereqs
    course_prereqs_el = course.query_selector('.coursedescadditional')
    # # get all prerequisite links and add their text to a list
    course_prereqs_a = course_prereqs_el.query_selector_all(
         'a') if course_prereqs_el else []
   # if not("Precludes") in course_prereqs_el.inner_text(): 
    prereqs_a_text = [req.inner_text() for req in course_prereqs_a]
    prereqs_a_text = [req.inner_text().replace('\xa0', ' ') for req in course_prereqs_a]
   # print("code "+course_code)
    prereqs = []
    prereqs = get_prereqs(course_prereqs_el, prereqs_a_text, course_code)

   

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
