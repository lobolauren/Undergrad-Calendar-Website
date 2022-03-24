README for 3760 Project - Team 2, UoGuelph W22

# Sprint 7

## Installation

```bash
sudo sh install.sh
cd course-utility
npm install
```

## Running Dev Server

```bash
cd course-utility
npm start

# in a seperate terminal:
cd api
flask run
```

## Create Production Build

> nginx points to the build folder, so the following must be run to show up on web page.

```bash
cd course-utility
npm run build
```

### Run Production Build

Follow the steps included in `config-file-example`.


## Running automated tests

Automated tests are done using crontab to run the tests script (/tests/test_main.py) every 30 minutes

### Set up crontab for your user account

`crontrab -e` 
or
`sudo crontab -e <username>` (for non sudo users)

 - Select a text editor
 - Modify the crontab file
    - You may copy the text from the given file or create a custom crontab 