from playwright.sync_api import sync_playwright
import time

# change this if running on a different server
url_to_use = 'https://131.104.49.102'

# goes to the site with playwright and checks if the url is valid
def test_home():

    site_running = True

    # start playwright
    with sync_playwright() as pw:

        browser = pw.chromium.launch(headless=True)
        # ignore self signed https error (connection not private) since we have a fake https
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        # try to go to the page, if failed, return false
        try:
            page.goto(url_to_use)
        except:
            site_running = False

        browser.close()

    return site_running


# tests the course-search page by clicking the search button, returns false if nothing is returned or it takes too long
def test_course_submit():

    button_working = True

    # start playwright
    with sync_playwright() as pw:

        browser = pw.chromium.launch(headless=True)
        # ignore self signed https error (connection not private) since we have a fake https
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        # try to go to the page, if failed, return false
        try:
            page.goto(url_to_use+'/coursesearch')
        except:
            browser.close()
            return False

        course_search = page.query_selector('.courseSearch')

        # fill in the form so it doesnt take too long (cis*2500 by default)
        page.fill('#courseCode', 'cis*2500')

        button_submit = course_search.query_selector('.btn')
   
        button_submit.click()

        # give the submit time to load (1 second by default - it shouldnt take that long)
        time.sleep(1)

        # check if the search returned anything
        courses = page.query_selector('.courseblock')
        if not courses:
            button_working = False

        browser.close()

    return button_working


# tests the make-graph page by clicking the graph button, returns false if nothing is returned or it takes too long
def test_graph_submit():

    button_working = True

    # start playwright
    with sync_playwright() as pw:

        browser = pw.chromium.launch(headless=True)
        # ignore self signed https error (connection not private) since we have a fake https
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        # try to go to the page, if failed, return false
        try:
            page.goto(url_to_use+'/makegraph')
        except:
            browser.close()
            return False

        # fill in the form so it doesnt take too long (cis*2500 by default)
        page.fill('#courseCode', 'cis*2500')

        # go to the correct button
        button_submit = page.query_selector('.btn-primary')

        button_submit.click()

        # give page time to navigate (2 seconds)
        time.sleep(2)

        # check that we went to the correct url
        if not page.url == (url_to_use+'/graph/course/cis*2500'):
            button_working = False

        browser.close()

    return button_working
