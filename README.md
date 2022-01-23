README for 3760 Project

# Sprint 1

## Running the scraper:

NOTE: Playwright or Chromium must be installed and updated prior to running this python program.

``` 
python scraper.py
```
- Generates a JSON file called ```course_info.json``` containing all the course data from https://calendar.uoguelph.ca/undergraduate-calendar/course-descriptions/.

## Running the CLI:

NOTE: Must be ran after the scraper program!
```
python cli.py
```
- Follow the command line interface to search for your desired course at UoG

## Running the unit tests:
```
cd tests
python test_scraper.py
```
- Tests for the web scraper functions
