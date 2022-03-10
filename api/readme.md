# Flask and uWSGI readme

# Instilation
Commands:
`python3 -m venv apiVENV`
`source apiVENV/bin/activate`
`apt-get install python3-all-dev`
`pip install wheel`
`pip install uwsgi flask`

Add api_start.service to the 'etc/systemd/system/' folder

# Config
in the api folder

Run Flask..
`flask run`

Run uWSGI..
`uwsgi --ini app.ini`

Run uWSGI server as daemon..
`sudo systemclt start api_start.service`