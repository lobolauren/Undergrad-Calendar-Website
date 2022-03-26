from test_api import *
from test_site import *
from email_ import *

import time

from dotenv import load_dotenv
import os

# load env variables from file if you want (set in a .env file)
load_dotenv()

# by default set as environment variables
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

# run testing code
def main():

    # api tests
    url_test = test_base_url()
    get_course_test = test_get_course()
    get_courses_test = test_get_courses()

    # site tests
    home_test = test_home()
    course_submit_test = test_course_submit()
    graph_submit_test = test_graph_submit()

    test_arr = [url_test, get_course_test, get_courses_test, home_test, course_submit_test, graph_submit_test]

    curr_time = time.ctime(time.time())

    out_str = f'''
            Date: {curr_time}
            
            API Status:
                Base URL Working: {url_test}
                get_course Working: {get_course_test}
                get_courses Working: {get_courses_test}
            
            Site Status:
                Home Page Working: {home_test}
                Course Search Working: {course_submit_test}
                Make Graph Working: {graph_submit_test}
            '''

    # if any test failed, send an email
    for t in test_arr:
        if t == False:
            send_email(RECEIVER_EMAIL, SENDER_EMAIL,
                       SENDER_PASSWORD, "CIS*3760 - Team 2, Server Status Fail Detected", out_str)
            pass # remove this line when email sent

    print(out_str)


if __name__ == '__main__':
    main()
