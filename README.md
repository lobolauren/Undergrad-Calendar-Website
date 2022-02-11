README for 3760 Project - Team 2, UoGuelph W22

# Sprint 4

Requirements:
 - Python version 3.x + pip
 - Playwright 
 - Chromium
 - Graphviz

NOTE: If python 2 is installed on the system, the user may have to use `python3`/`pip3` instead of `python`/`pip`

#### Install sh
``` 
pip install sh
``` 
#### Install Requirements
```
sh install.sh
```
### If above does not work:
#### Install Python Libraries
``` 
pip install -r requirements.txt
```
#### Chromium install (apt: debian-based systems)
``` 
sudo apt-get install chromium
```
#### Install Graphviz (apt: debian-based systems)
```
sudo apt install graphviz
```
#### Install Graphviz (apt: debian-based systems)
```
sudo apt install graphviz
```

## Running the scraper:
### Scraping Guelph courses
- Run scraper.py program to get information about UoGuelph courses 
``` 
python scraper.py
```

- Generates a JSON file called ```course_info.json``` containing all the course data from https://calendar.uoguelph.ca/undergraduate-calendar/course-descriptions/.

### Scrapping Carleton courses
- Run scraper.py program to get information about Carleton courses 
``` 
python scraper_carleton.py
```

- Generates a JSON file called ```course_info_carleton.json``` containing all the course data from https://calendar.carleton.ca/undergrad/courses/.

## Running the CLI:
 - Run this after running scraper.py, or if the course_info.json or the course_info_carleton.json file already exists.
```
python main.py
```
 - The user can then follow command prompts from the program
 - By default, the CLI runs with the Guelph course data.
 - Running the CLI with Carleton courses:
```
python main.py course_info_carleton.json
```
#### Commands:

- `coursesearch` search for courses at UoG
  - includes search parameters such as course title, code, term, weight
    - code: [dept]\*[code] or [dept] or [code]
    - ex. 'CIS\*3090', 'cis', '1000'
  - Will display a list of all courses found that fit the search criteria
- `makegraph` create prerequsite graph for UoG or Carleton
  - The makegraph command can be launched with any of these command line options:
    - '-d' allows graphing a department
    - '-p' allows graphing a program
    - '-c' allows graphing a course
    - '-C' allows creating a catalogue of all the courses or subjects
    - '-o' allows naming the output for the output file
  - The user can enter a course name 
    - (format: [dept]*[code] ex. 'CIS\*3090')
  - Or a department code (ex. 'cis')
  - Or minor/major code (ex. 'CS', 'CS:C' or 'ANTH')
  - The program then generates a graphic representation of the prerequisite tree for the given course/department, & saves it in a pdf file in the *graph-output* folder
- `quit` quits the program

### Running the unit tests:
```
cd tests
pytest # Runs all the pytest unit tests
```
- Tests for the web scraper/graph functions

## Graphing Limitations
  - The program does not have indicators for 'pick 2+ of ...' prerequisite options
  - Does not indicate '[course or (course or course)]' cases
  - A graph edge may indicate a '1 of...' case when there is only one prerequisite for that colour
    - This is because the other option(s) either no longer exist, or aren't a course 
    - (ex. '[course] or experience in field')
  - Graphs of degree programs do not include elective credits, or indicate when there is more than one option of courses to take
  - In cases where a prerequisite is either a high school course or a university course, the graph may show the university course as a sole prerequisite when it is not (because high school courses are not parsed as they dont exist)
    - ex. STAT*2040, for the cs degree, stat*2040 appears to have a prerequisite that is not required by the degree, which is impossible
