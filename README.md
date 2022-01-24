README for 3760 Project - Team 2, W22

# Sprint 1

NOTE: Requires python version 3+, Playwright and Chromium must be installed and updated prior to running this python program.
- Playwright install: 
``` 
pip install playwright (or pip3 install playwright)
playwright install
```
- Chromium install (for debian-based systems)
``` 
sudo apt-get install chromium
```

## Running the scraper:
``` 
python scraper.py
```
Or (if python 2 is installed or 'python' does not work)
``` 
python3 scraper.py
```
- Generates a JSON file called ```course_info.json``` containing all the course data from https://calendar.uoguelph.ca/undergraduate-calendar/course-descriptions/.

## Running the CLI:

NOTE: Must be ran after the scraper program!
```
python cli.py
```
Or (if python 2 is installed or 'python' does not work)
``` 
python3 cli.py
```

- Follow the command line interface to search for your desired course at UoG

## Running the unit tests:
```
cd tests
python test_scraper.py
```
- Tests for the web scraper functions

# Sprint 2
