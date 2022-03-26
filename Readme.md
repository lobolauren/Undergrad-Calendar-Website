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

 - Set environment variables in a .env file in the tests folder (create the .env file)
   -  RECEIVER_EMAIL=?
      SENDER_EMAIL=?
      SENDER_PASSWORD=?
   - Alternatively, you may modify the `test_main.py` file to set globals

### Set up crontab for your user account

`crontrab -e` 
or
`sudo crontab -e <username>` (for non sudo users)

 - Select a text editor
 - Modify the crontab file accordingly:

    #### Copy the below line into the crontab file after running crontab -e 

    `0,30 * * * * python3 /home/sysadmin/3760-project/tests/test_main.py > /home/sysadmin/3760-project/course-utility.log`

    #### !NOTE! : replace the path of the `test_main.py` & `course-utility.log` files with the correct path for your system
    #### This line runs the script every 30 minutes & outputs the latest results to `course-utility.log`

