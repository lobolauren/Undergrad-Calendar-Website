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
in the api folder..
the app.ini is the config file for uWSGI

# Running

Run Flask..
`flask run`

Run uWSGI..
`uwsgi --ini app.ini`

Run uWSGI server as daemon..
`sudo systemctl start api_start.service`
file on VM is `sudo systemctl start siteapi.service`