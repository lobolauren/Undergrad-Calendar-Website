import json
from posixpath import split
from typing import List, final
from playwright.sync_api import sync_playwright


# scrapes page for all coruse codes (ex. CIS, MATH, AGGR)
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


# get individual course details from course object
def get_course_details(course):

    course_code_el = course.query_selector('.detail-code')
    course_code = course_code_el.inner_text()

    course_title_el = course.query_selector('.detail-title')
    course_title = course_title_el.inner_text()

    course_offerings_el = course.query_selector('.detail-typically_offered')
    course_offerings = course_offerings_el.inner_text() if course_offerings_el else ''

    course_prereqs_el = course.query_selector('.detail-prerequisite_s_ span') 
    course_prereqs_a = course_prereqs_el.query_selector_all('a') if course_prereqs_el else []

    final_prereqs = [req.inner_text() for req in course_prereqs_a]

    prereqs = {
        'reg_prereqs': [],
        'eq_prereqs': []
    }

    #search list of prereqs to check if in a '1 of' block
    if course_prereqs_el:
        prereq_text = course_prereqs_el.inner_text()

        #remove commas inside brackets
        inside_brackets = False
        new_str = ''
        for c in prereq_text:
            if c == ')':
                inside_brackets = False
            if not inside_brackets or (inside_brackets and c != ','):
                new_str += c
            if c == '(':
                inside_brackets = True

        prereq_text = new_str

        sub_prereq_text = prereq_text.split(',')

        ftr = lambda s: True if '(' in s or '[' in s else False

        eq_prereqs = list(filter(ftr,sub_prereq_text))

        if not eq_prereqs and ('or' in prereq_text or 'of' in prereq_text):
            prereqs['eq_prereqs'] = [final_prereqs]

        else:

            final_prereqs_copy = final_prereqs[:]

            #for each 'block' of prerequisits, check if any codes from the full list are contained in it, if so, add to the eq_prereqs list
            for sub in eq_prereqs:
                sub_list = []

                for code in final_prereqs:

                    if code in sub:
                        sub_list.append(code)
                        #double checking
                        if code in final_prereqs_copy:
                            final_prereqs_copy.remove(code)

                prereqs['eq_prereqs'].append(sub_list)
            
            prereqs['reg_prereqs'] = final_prereqs_copy

        #consistency for courses that no longer exist (and therefore dont appear in the full list)
        #ex. ([existing*course] or [doesnt*exist]), put existing course in reg_prereqs list

        eq_prereqs_copy = prereqs['eq_prereqs'][:]

        idx = 0
        for block in eq_prereqs_copy:

            if len(block) < 2:

                if block:
                    prereqs['reg_prereqs'].append(block[0])
                prereqs['eq_prereqs'].pop(idx)
                idx -= 1
            idx += 1


    course_terms = []
    if 'fall' in course_offerings.lower():
        course_terms.append('F')
    if 'winter' in course_offerings.lower():
        course_terms.append('W')
    if 'summer' in course_offerings.lower():
        course_terms.append('S')

    course_weight_el = course.query_selector('.detail-hours_html')
    course_weight = float(course_weight_el.inner_text()[1:-1])

    course_desc_el = course.query_selector('.courseblockextra')
    course_desc = course_desc_el.inner_text() if course_desc_el else ''

    return {
        'code': course_code.upper(),
        'name': course_title,
        'terms': course_terms,
        'weight': course_weight,
        'description': course_desc,
        'prereqs': prereqs
    }


# scrape course information from the university website
def get_course_info(course_codes: List[str]):

    course_info = {}

    with sync_playwright() as pw: 

        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()

        for code in course_codes:
            course_info[code] = []
            page.goto(f'https://calendar.uoguelph.ca/undergraduate-calendar/course-descriptions/{code}/')

            courses = page.query_selector_all('.courseblock')
            for course in courses:
                course_info[code].append(get_course_details(course))
            

        browser.close()

    return {'courses': course_info}


# save dictionary object to a JSON file
def save_dict_as_json(dict, filename):
    with open(filename, 'w') as fp:
        json.dump(dict, fp, indent=4)


def main():
    print("Scraping...")
    codes = get_course_codes()
    print("Getting course info... (this may take a minute)")
    course_info = get_course_info(codes)
    print("Saving file...")
    save_dict_as_json(course_info, filename='course_info.json')
    print("Done.")


if __name__ == '__main__':
    main()
