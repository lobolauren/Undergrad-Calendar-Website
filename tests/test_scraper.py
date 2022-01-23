import unittest
import os
import json
import test_constants
# imports the scraper directory in the directory above the tests
import sys
sys.path.insert(0, '../')
import scraper

class TestScraper(unittest.TestCase):

    def test_getCourseCodeFunction(self):
        courseCodes = scraper.get_course_codes()
        self.assertIsNotNone(courseCodes)
        self.assertEqual(len(courseCodes), test_constants.NUM_COURSE_CODES)
        self.assertEqual(courseCodes[0], test_constants.TEST_COURSE_CODE)

    def test_getCourseInfo(self):
        # test scrapper with one course only
        course_info = scraper.get_course_info(test_constants.TEST_COURSE)
        self.assertIsNotNone(course_info)

        courses = course_info[test_constants.COURSES_CONSTANT]
        accountingCourses = courses[test_constants.TEST_COURSE_CODE]
        self.assertIsNotNone(courses)

        introAccounting = accountingCourses[0]
        self.assertIsNotNone(introAccounting)
        self.assertEqual(introAccounting["code"], "ACCT*1220")
        self.assertEqual(introAccounting["name"], "Introductory Financial Accounting")
        self.assertEqual(introAccounting["terms"], ["F", "W"])
        self.assertEqual(introAccounting["weight"], 0.5)

    def test_saveDictAsJSON(self):
        try:
            scraper.save_dict_as_json(test_constants.TEST_DICT, test_constants.TEST_FILENAME)
            with open(test_constants.TEST_FILENAME, 'r') as testFile:
                contents = testFile.read()
        finally:
            os.remove(test_constants.TEST_FILENAME) # delete JSON once done
        self.assertIsNotNone(contents)
        # convert to dictionary
        jsonObject = json.loads(contents)
        self.assertEqual(jsonObject, test_constants.TEST_DICT)
        

if __name__ == '__main__':
    unittest.main() # allows you to run by doing python3 testScraper.py