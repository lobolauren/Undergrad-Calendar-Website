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

        page.goto('https://calendar.uoguelph.ca/undergraduate-calendar/course-descriptions/')

        # select part of page containing links to course codes
        codes_region = page.query_selector('.az_sitemap')
        codes = codes_region.query_selector_all('li')[27:] # ignore first 27 because they are just letters of the alphabet for navigation

        # codes are formatted as such: ex. Chemistry (CHEM), we want just CHEM
        for code in codes: 
            code_str = code.inner_text()
            # finds index of first bracket, grabs string between that index and the last character
            code_str_final = code_str[code_str.index('(')+1:-1] 
            codes_list.append(code_str_final.lower())

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

# given a string containg '4U', will return a list of high school course names
def get_hs_course(prereq_text=""):
    course_li = prereq_text.split(" ")

    hs_courses = []
    # for every word
    for i, el in enumerate(course_li):
        if "4U" in el:
            j = i
            temp_str = ''
            # go through the list and build the course string until it is over
            while j < len(course_li) and course_li[j] != "or":
                
                temp_str += course_li[j] + ' '
                # if there is a comma, the course string is done, but still include that word
                if ',' in course_li[j]:
                    break
                
                j += 1
            # get rid of unwanted characters
            temp_str = ((temp_str.replace('(', '')).replace(')','')).replace(',', '')
            hs_courses.append(temp_str)
    
    return hs_courses


def get_prereqs(prereqs_el, prereqs_list, course_code):

    prereqs = {
        'reg_prereqs': [],
        'eq_prereqs': [] # list of lists each sublist represents related prerequisites
    }

    if prereqs_el:
        prereq_text = prereqs_el.inner_text()
        
        # if there are highschool courses
        if "4U" in prereq_text:
            hs_courses = get_hs_course(prereq_text)
            
            # add highschool courses to the list of prerequisites
            for hs_course in hs_courses:
                prereqs_list.append(hs_course)


        # the reason we do this is because we noticed that every block of related prerequisites is contained within 
        # brackets that are seperated by commas. We then remove the commas from between the brackets so we can seperate
        # each block of related prerequisites by splitting on the comma character
        prereq_text = remove_commas_between_brackets(prereq_text)
        tokens = prereq_text.split(',')

        # we now only want to look at courses that are in a block of related prerequisites so we get all the blocks that
        # contain the bracket characters
        ftr = lambda s: True if '(' in s or '[' in s else False
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


# get individual course details from course object
def get_course_details(course):

    # get text for each element
    course_code = get_element_text(course, '.detail-code')
    course_title = get_element_text(course, '.detail-title')
    course_availability = get_element_text(course, '.detail-typically_offered')
    course_desc = get_element_text(course, '.courseblockextra')
    course_restrictions = get_element_text(course, '.detail-restriction_s_ span')
    course_department = get_element_text(course, '.detail-department_s_ span')
    course_location = get_element_text(course, '.detail-location_s_ span')
    course_corequisites = get_element_text(course, '.detail-co_requisite_s_ span')
    course_offering = get_element_text(course, '.detail-offering span')
    de_offering = True if 'distance education' in course_offering.lower() else False
    course_weight = float(get_element_text(course, '.detail-hours_html')[1:-1])

    course_terms = []
    if 'fall' in course_availability.lower():
        course_terms.append('F')
    if 'winter' in course_availability.lower():
        course_terms.append('W')
    if 'summer' in course_availability.lower():
        course_terms.append('S')

    course_prereqs_el = course.query_selector('.detail-prerequisite_s_ span')
    # get all prerequisite links and add their text to a list
    course_prereqs_a = course_prereqs_el.query_selector_all('a') if course_prereqs_el else []
    prereqs_a_text = [req.inner_text() for req in course_prereqs_a]
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
            if code == 'iaef': # edge case since the url for the course descriptions is wrong
                page.goto(f'https://calendar.uoguelph.ca/undergraduate-calendar/course-descriptions/ieaf/')
            else:
                page.goto(f'https://calendar.uoguelph.ca/undergraduate-calendar/course-descriptions/{code}/')

            print("  Scraping \'"+code+"\' courses...", end='', flush=True)
            # select every course on the page, loop through and get details
            courses = page.query_selector_all('.courseblock')
            for course in courses:
                course_info[code].append(get_course_details(course))

            print(" Done")

        browser.close()

    return course_info


# https://calendar.uoguelph.ca/undergraduate-calendar/degree-programs/
def get_degree_program_links(page: Page):
    
    page.goto('https://calendar.uoguelph.ca/undergraduate-calendar/degree-programs/')

    list_els = page.query_selector_all('.sitemap li a')
    # get the link for each degree program page from the main page
    links = []
    for list_el in list_els:
        # get the href for each program
        relative_link = list_el.get_attribute("href")
        links.append(f'https://calendar.uoguelph.ca{relative_link}')

    return links

# Takes degree links returned from get_degree_program_links() and builds a dict of bachelors and their corresponding programs
def get_bachelor_programs(page: Page, degree_links):
    bachelor_programs = {}
    # navigate the page for each degree
    for degree_link in degree_links:
        degree_link += '#programstext'
        page.goto(degree_link)

        # Getting Bachelor degree title
        title_el = page.query_selector('.page-title')
        bachelor = title_el.inner_text()
        # the object at the location of the bachelor (ex. BCOMP)
        bachelor_programs[bachelor] = []
        
        # every list with a hyperlink in sitemap
        list_els = page.query_selector_all('.sitemap li a')
        # make a list of each degree
        for list_el in list_els:            
            bach_prog = list_el.inner_text()
            # get the code for each degree
            bach_prog = bach_prog[:bach_prog.index('(')].rstrip() # get everything between the brackets
            bachelor_programs[bachelor].append(bach_prog)

    return(bachelor_programs)


# ex: https://calendar.uoguelph.ca/undergraduate-calendar/degree-programs/bachelor-applied-science-basc/#programstext
def get_program_majors(page: Page, degree_links): # Bachelor degree programs of Arts and Science

    degree_programs_links = []
    # each program on the page for each degree
    for degree_link in degree_links:
        degree_link += '#programstext'
        page.goto(degree_link)
        
        # navigate through each hyperlink and get the link to all the programs in the degree
        list_els = page.query_selector_all('.sitemap li a')
        # degree_programs_links = []
        for list_el in list_els:
            relative_link = list_el.get_attribute("href") # getting the link
            degree_programs_links.append(f'https://calendar.uoguelph.ca{relative_link}')

    return(degree_programs_links)

# ex: https://calendar.uoguelph.ca/undergraduate-calendar/programs-majors-minors/applied-human-nutrition-ahn/#requirementstext
def get_major_requirements(page: Page, links, bach_programs): # Specific major program
    
    programs_reqirements = {}
    # for every degree link
    for degree_programs_link in links:
        # navigate to list of courses
        degree_programs_link += '#requirementstext'
        page.goto(degree_programs_link)
        
        # getting info
        title_el = page.query_selector('.page-title')
        title = title_el.inner_text()
        code = title[title.index('(')+1:-1].lower() # finds index of first bracket, grabs string between that index & the last character
        title = title[:title.index('(')].rstrip()

        # Sometimes there are programs in different degrees that have the same code and same courses, avoid duplicates
        if code in programs_reqirements.keys():
            print(f'{code} is duplicate')
            continue

        # Finding Bachelor that belongs to program
        bachelor_title = None
        for bach, progs in bach_programs.items():
            for prog in progs:
                if prog == title:
                    bachelor_title = bach

        # final object
        programs_reqirements[code] = {
            'title' : title,
            'bachelor': bachelor_title,
            'major_reqs':[],
            'minor_reqs':[]
        }

        print("  Scraping \'"+code+"\' requirements...", end='', flush=True)

        # selects table of Major requirement on each degree page
        table = page.query_selector('h2:text("Major") ~ .sc_courselist') 
        if table: # only if the table exists
            rows = table.query_selector_all('tr:not(areaheader)') #parse first column of table for course codes
            # parse every row in the column for hyperlinks (courses that exist)
            for row in rows:
                course_el = row.query_selector('a')
                # if the course exists, add it to the major reqs list
                if course_el:
                    course_code = course_el.inner_text()
                    if len(course_code) < 10: #skip course requirments that are not courses
                        programs_reqirements[code]['major_reqs'].append(course_code)
        
        # selects table of minor requirement on each degree page
        table = page.query_selector('h2:text("Minor") ~ .sc_courselist') 
        if table:  # only if the table exists
            rows = table.query_selector_all('tr:not(areaheader)')
            # parse every row in the column for hyperlinks (courses that exist)
            for row in rows:
                course_el = row.query_selector('a')
                # if the course exists, add it to the minor reqs list
                if course_el:
                    course_code = course_el.inner_text()
                    if len(course_code) < 10:
                        programs_reqirements[code]['minor_reqs'].append(course_code)
        print('Done')

    return programs_reqirements

def get_program_info():
    # start playwright
    with sync_playwright() as pw: 

        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()

        print('Getting degree programs')
        degree_links = get_degree_program_links(page)
        bach_programs = get_bachelor_programs(page, degree_links)
        program_links = get_program_majors(page, degree_links)

        print('Getting program requirements')
        program_info = get_major_requirements(page, program_links, bach_programs)

        browser.close()

    return program_info


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

    print("Scraping program info")
    program_info = get_program_info()
    
    # object contains two lists
    data = {
        "programs": program_info,
        "courses": course_info
    }

    print("Saving file...")
    save_dict_as_json(data, filename='course_info.json')

    end = time.time()
    if debug:
        print(f"Done in {int(end - start)}s.")


if __name__ == '__main__':
    main()
