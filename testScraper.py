import unittest
import os
import json
from testConstants import NUM_COURSE_CODES, TEST_DICT, TEST_FILENAME, TEST_COURSE_CODE, TEST_COURSE
import scraper

class TestScraper(unittest.TestCase):

    def test_getCourseCodeFunction(self):
        courseCodes = scraper.get_course_codes()
        self.assertIsNotNone(courseCodes)
        self.assertEqual(len(courseCodes), NUM_COURSE_CODES)
        self.assertEqual(courseCodes[0], TEST_COURSE_CODE)

    def test_getCourseInfo(self):
        # test scrapper with one course only
        course_info = scraper.get_course_info(TEST_COURSE)
        self.assertIsNotNone(course_info)

        courses = course_info[TEST_COURSE_CODE.upper()]
        self.assertIsNotNone(courses)

        introAccounting = courses[0]
        self.assertIsNotNone(introAccounting)
        self.assertEqual(introAccounting["code"], "ACCT*1220")
        self.assertEqual(introAccounting["name"], "Introductory Financial Accounting")
        self.assertEqual(introAccounting["terms"], ["F", "W"])
        self.assertEqual(introAccounting["weight"], 0.5)

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