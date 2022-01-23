import json
from typing import List
from playwright.sync_api import sync_playwright

#scrapes page for all coruse codes (ex. CIS, MATH, AGGR)
def get_course_codes():

    codes_list = []

    #Using synchronus playwright
    with sync_playwright() as pw:
        #launch chromium headless
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(
            f'https://calendar.uoguelph.ca/undergraduate-calendar/course-descriptions/')

        #select part of page containing links to course codes
        codes_region = page.query_selector('.az_sitemap')
        codes = codes_region.query_selector_all('li')[27:] #select all lists (ignore first 27, which are letters of the alphabet)
        #for each code in the list of names
        for code in codes: 

            code_str = code.inner_text()
            #extract the code from the text
            code_str_final = code_str[code_str.index('(')+1:-1] #finds index of first bracket, grabs string between that index & the last character
            #add code to the list in lower case (for navigation on the website)
            codes_list.append(code_str_final.lower())

        browser.close()

    return codes_list


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

                course_desc_el = course.query_selector('.courseblockextra')
                course_desc = course_desc_el.inner_text() if course_desc_el else ''

                course_info[code].append({
                    'code': course_code.upper(),
                    'name': course_title,
                    'terms': course_terms,
                    'weight': course_weight,
                    'description': course_desc,
                })

        browser.close()

    return {
        'courses': course_info
    }


def save_dict_as_json(course_info, filename):
    with open(filename, 'w') as fp:
        json.dump(course_info, fp, indent=4)


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
