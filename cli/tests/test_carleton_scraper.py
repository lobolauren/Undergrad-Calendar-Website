import unittest
import test_constants
# imports the scraper directory in the directory above the tests
import sys
sys.path.insert(0, '../')
import scraper_carleton

class TestCarletonScraper(unittest.TestCase):

    def test_get_course_code_function(self):
        # gets list of all course codes and compares with expected amount
        course_codes = scraper_carleton.get_course_codes()
        assert course_codes != None
        assert len(course_codes) == test_constants.CARLETON_COURSE_CODES
        assert course_codes[0] == "aero"
        assert course_codes[2] == "asla"
        assert course_codes[len(course_codes) - 1] == "wgst"


    def test_get_prerequisites(self):
        course_info = scraper_carleton.get_course_info(["AERO", "ARAB"])
        assert course_info != None

        # ARAB*3020
        eq_list = ["ARAB*3010", "ARAB*3015"]
        arab_courses = course_info["ARAB"]
        arab_3020_index = 4
        arab_3020 = arab_courses[arab_3020_index]
        assert arab_3020["code"] == "ARAB*3020"
        assert arab_3020["prereqs"]["reg_prereqs"] == []
        assert arab_3020["prereqs"]["eq_prereqs"][0] == eq_list

        # AERO*3101
        req_prereqs = ["MAAE*3202"]
        aerospace_courses = course_info["AERO"]
        aero_3101_index = 2
        aero_3101 = aerospace_courses[aero_3101_index]
        assert aero_3101["code"] == "AERO*3101"
        assert aero_3101["prereqs"]["eq_prereqs"] == []
        assert aero_3101["prereqs"]["reg_prereqs"] == req_prereqs

if __name__ == '__main__':
    unittest.main() # allows you to run by doing python3 test_scraper.py