from flask import Flask
import json

app = Flask(__name__)

@app.route('/api/')
def hello():
    return 'Hello world!'

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

@app.route("/api/get_course_data/", methods=['GET'])
def get_course_data_json():
    return get_course_info("course_info.json")

if __name__ == '__main__':
    app.run(host='0.0.0.0')

