# Flask and uWSGI readme

## Installation
```bash
python3 -m venv env
source env/bin/activate
apt-get install python3-all-dev
pip install -r requirements.txt
```

See readme in `../config-file-example/` for further instructions

## Config
the `app.ini` is the config file for uWSGI

## Running

Run Flask: `flask run`

Run uWSGI: `uwsgi --ini app.ini`

Run uWSGI server as daemon: `sudo systemctl start api_start.service` (file on our VM is `sudo systemctl start siteapi.service`)
