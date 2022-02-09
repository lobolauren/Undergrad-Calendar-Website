import unittest
import os
import json
import test_constants
# imports the scraper directory in the directory above the tests
import sys
sys.path.insert(0, '../')
import scraper_carleton

class TestCarletonScraper(unittest.TestCase):

    def test_get_course_code_function(self):
        # gets list of all course codes and compares with expected amount
        courseCodes = scraper_carleton.get_course_codes()
        self.assertIsNotNone(courseCodes)
        self.assertEqual(len(courseCodes), test_constants.CARLETON_COURSE_CODES)
        self.assertEqual(courseCodes[0], "aero")
        self.assertEqual(courseCodes[2], "asla")
        self.assertEqual(courseCodes[len(courseCodes) - 1], "wgst")


if __name__ == '__main__':
    unittest.main() # allows you to run by doing python3 test_scraper.py