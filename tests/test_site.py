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
            browser.close()
            return False

        app = page.query_selector('.App')

        if not app:
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


        if course_search:

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
        else:
            button_working = False

        browser.close()

    return button_working


# tests the make-graph page by going to the graph link, returns false if nothing is returned or it takes too long
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
            page.goto(url_to_use+'/graph/guelph/course/cis*2500')
        except:
            browser.close()
            return False

        time.sleep(2)

        # check if we're on a graph page
        node = page.query_selector('.reactflow-container')

        if not node:
            button_working = False

    return button_working
