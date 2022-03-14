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
