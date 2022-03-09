README for 3760 Project - Team 2, UoGuelph W22

# Sprint 5

Requirements (for non-apt installs):
- NGINX
- npm/node.js
- bootstrap
- jquery

## Run Install Script (using apt)
```
`sudo sh install.sh`
```

## Install/start React App

Install: 
```
`cd course-utility`
`npm install`
```

Start Dev:
```
`npm start`
```

Build React Project:
- Nginx points to the build folder, so the following must be run if build directory is empty.
```
`npm run build`
```


## Nginx

Start:
`systemctl start nginx`

Stop:
`systemctl stop nginx`
