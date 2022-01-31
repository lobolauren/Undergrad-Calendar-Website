# Given a full course code (i.e. CIS*3760), return course attr (i.e. cis)
def get_course_attr(course_str: str, upper=False):
    if upper:
        return course_str[:course_str.index('*')].upper()
    else:
        return course_str[:course_str.index('*')].lower()


def get_course_number(course_str: str):
    return course_str[course_str.index('*')+1:]