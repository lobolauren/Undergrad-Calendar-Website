from math import degrees
import unittest
import os
import json
import test_constants
# imports the scraper directory in the directory above the tests
import sys
sys.path.insert(0, '../')
import scraper

class TestScraper(unittest.TestCase):

    def test_get_course_code_function(self):
        # gets list of all course codes and compares with expected amount
        courseCodes = scraper.get_course_codes()
        self.assertIsNotNone(courseCodes)
        self.assertEqual(len(courseCodes), test_constants.NUM_COURSE_CODES)
        self.assertEqual(courseCodes[0], test_constants.TEST_COURSE_CODE)

    def test_get_course_info(self):
        # test scrapper with one course only
        course_info = scraper.get_course_info(test_constants.TEST_COURSE)
        self.assertIsNotNone(course_info)
        accountingCourses = course_info[test_constants.TEST_COURSE_CODE]
        self.assertIsNotNone(course_info)

        # first accounting course must be AACT*1220
        introAccounting = accountingCourses[0]
        self.assertIsNotNone(introAccounting)
        self.assertEqual(introAccounting["code"], "ACCT*1220")
        self.assertEqual(introAccounting["name"], "Introductory Financial Accounting")
        self.assertEqual(introAccounting["terms"], ["F", "W"])
        self.assertEqual(introAccounting["weight"], 0.5)

    def test_save_dict_as_JSON(self):
        # save a test dictionary object using the functcion
        try:
            scraper.save_dict_as_json(test_constants.TEST_DICT, test_constants.TEST_FILENAME)
            with open(test_constants.TEST_FILENAME, 'r') as testFile:
                contents = testFile.read()
        finally:
            os.remove(test_constants.TEST_FILENAME) # delete JSON once done

        # convert to dictionary and compare with original dictionary
        self.assertIsNotNone(contents)
        jsonObject = json.loads(contents)
        self.assertEqual(jsonObject, test_constants.TEST_DICT)

    def test_requisites(self):
        # get test course info
        course_info = scraper.get_course_info(test_constants.TEST_COURSE)
        self.assertIsNotNone(course_info)
        #courses = course_info[test_constants.COURSES_CONSTANT]
        accountingCourses = course_info[test_constants.TEST_COURSE_CODE]

        #Check reg_prereqs and eq_prereqs empty
        acct1220Index = 0
        acct1240Index = 1
        self.assertEqual(accountingCourses[acct1220Index]["code"], "ACCT*1220")
        self.assertEqual(accountingCourses[acct1220Index]["prereqs"]["reg_prereqs"], [])
        self.assertEqual(accountingCourses[acct1220Index]["prereqs"]["eq_prereqs"], [])

        # Check reg_prereqs
        self.assertEqual(accountingCourses[acct1240Index]["code"], "ACCT*1240")
        self.assertEqual(accountingCourses[acct1240Index]["prereqs"]["reg_prereqs"][0], "ACCT*1220")
        self.assertEqual(accountingCourses[acct1240Index]["prereqs"]["eq_prereqs"], [])

        # Check eq_prereqs lists
        #courses = course_info[test_constants.COURSES_CONSTANT]
        agrCourses = course_info[test_constants.TEST_COURSE_CODE_AGR]

        agr2050Index = 1
        firstEqList = ["AGR*1110","AGR*2150"]
        secondEqList = ["BIOL*1050","BIOL*1070"]
        self.assertEqual(agrCourses[agr2050Index]["code"], "AGR*2050")
        self.assertEqual(agrCourses[agr2050Index]["prereqs"]["reg_prereqs"], [])
        self.assertEqual(agrCourses[agr2050Index]["prereqs"]["eq_prereqs"][0][0], "AGR*1110")
        self.assertEqual(agrCourses[agr2050Index]["prereqs"]["eq_prereqs"][0][1], "AGR*2150")
        self.assertEqual(agrCourses[agr2050Index]["prereqs"]["eq_prereqs"][0], firstEqList)
        self.assertEqual(agrCourses[agr2050Index]["prereqs"]["eq_prereqs"][1][0], "BIOL*1050")
        self.assertEqual(agrCourses[agr2050Index]["prereqs"]["eq_prereqs"][1][1], "BIOL*1070")
        self.assertEqual(agrCourses[agr2050Index]["prereqs"]["eq_prereqs"][1], secondEqList)

    def test_get_program_info(self):
        # gets list of all major requirements and compares with expected amount
        program_info = scraper.get_program_info()
        self.assertIsNotNone(program_info)
        self.assertEqual(len(program_info), test_constants.NUM_PROGRAMS_MAJORS)
        self.assertEqual(program_info["ahn"]["title"], test_constants.TEST_MAJOR_NAME)
        self.assertEqual(program_info["ahn"]["major_reqs"][0], test_constants.TEST_MAJOR_REQ)




if __name__ == '__main__':
    unittest.main() # allows you to run by doing python3 test_scraper.py