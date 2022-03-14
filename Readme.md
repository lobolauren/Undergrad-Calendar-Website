README for 3760 Project - Team 2, UoGuelph W22

# Sprint 6

Requirements (for non-apt installs):
- NGINX
- npm/node.js
- bootstrap
- jquery

## Run Install Script (using apt)
```
`sudo sh install.sh`
`cd course-utility`
`npm install`
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

flask-cors-3.0.10


## uWSGI/Flask
Install..
`sudo sh install.sh`
for more details check the api folder readme

Config..
in the api folder..
the app.ini is the config file for uWSGI
in the config-file-example folder..
Add api_start.service from the config folder to the 'etc/systemd/system/' folder

To Test..
Run Flask..
`flask run`
Run uWSGI..
`uwsgi --ini app.ini`

For Production..
Run uWSGI server as daemon..
`sudo systemctl start api_start.service`
file on VM is `sudo systemctl start siteapi.service`