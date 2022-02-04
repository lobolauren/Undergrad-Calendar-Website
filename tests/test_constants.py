# Scraper test constants
NUM_COURSE_CODES = 86
NUM_PROGRAMS_MAJORS = 159
TEST_DICT = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 2020
}
TEST_FILENAME = "test.json"
COURSES_CONSTANT = "courses"

TEST_COURSE_CODE = "acct"
TEST_COURSE_CODE_AGR = "agr"
TEST_COURSE = [TEST_COURSE_CODE, TEST_COURSE_CODE_AGR]

# programs section of course data JSON
TEST_PROGRAM_NAME = "ahn"
TEST_MAJOR_NAME = "Applied Human Nutrition"
TEST_MAJOR_REQ = "CHEM*1040"
TEST_PROGRAM = [TEST_PROGRAM_NAME, TEST_MAJOR_NAME, TEST_MAJOR_REQ]

# Test makegraph constants
PROGRAMS = {
  "cs": {
            "title": "Computer Science",
            "major_reqs": [
                "CIS*1300",
                "CIS*1910",
                "MATH*1200",
                "CIS*2500",
                "CIS*2910",
                "MATH*1160",
                "CIS*2030",
                "CIS*2430",
                "CIS*2520",
                "CIS*2750",
                "CIS*3110",
                "CIS*3490",
                "CIS*3150",
                "CIS*3750",
                "STAT*2040",
                "CIS*3760",
                "CIS*4650"
            ],
            "minor_reqs": []
        }
}