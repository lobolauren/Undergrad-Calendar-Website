# function to open JSON file
def get_course_info(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read()
            coursedata = json.loads(data)
    # if the file isnt found, return nothing
    except FileNotFoundError as e:
        return {}
    return coursedata