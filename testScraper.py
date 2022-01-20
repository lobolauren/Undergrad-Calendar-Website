import unittest
import os
import json
from testConstants import NUM_COURSE_CODES, TEST_DICT, TEST_FILENAME, TEST_COURSE_CODE
import scraper

class TestScraper(unittest.TestCase):

    # Needs course_codes.txt for test to run
    def test_getCourseCodeFunction(self):
        courseCodes = scraper.get_course_codes()
        self.assertIsNotNone(courseCodes)
        self.assertEqual(len(courseCodes), NUM_COURSE_CODES)

    # Takes a long time to run
    def test_getCourseInfo(self):
        codes = scraper.get_course_codes()
        # test scrapper with one course only
        course_info = scraper.get_course_info(TEST_COURSE_CODE)
        self.assertIsNotNone(course_info)

    def test_saveDictAsJSON(self):
        try:
            scraper.save_dict_as_json(TEST_DICT, TEST_FILENAME)
            with open(TEST_FILENAME, 'r') as testFile:
                contents = testFile.read()
        finally:
            os.remove(TEST_FILENAME) # delete JSON once done
        self.assertIsNotNone(contents)
        # convert to dictionary
        jsonObject = json.loads(contents)
        self.assertEqual(jsonObject, TEST_DICT)
        

if __name__ == '__main__':
    unittest.main() # allows you to run by doing python3 testScraper.py