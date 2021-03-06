# Config README

> Currently, the site shows as "Not Secure" due to the SSL Certificate being self signed

## Setup

- Add the `api_start.service` from the config folder (`../config-file-example/api_start.service`) to the `/etc/systemd/system/` directory
- Add the config file from the config folder (`../config-file-example/131.104.49.102`) to the `/etc/nginx/sites-available` directory
- Create a symoblic link from the file you just added to the `/etc/nginx/sites-enabled/` directory using:

```bash
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
```

- start/restart nginx

```bash
sudo systemctl restart nginx
```
> NOTE: use restart whenever you make changes to the config files for nginx

- start the uWSGI process using:

```bash
sudo systemctl start api_start.service
```

## Logs
- Find the access log at /var/log/nginx/access.log
- Find the error log at /var/log/nginx/error.log
- In order to read the log files, use the following command:
```
`sudo vi <log>`
```

## Add the SSL certificate and key
1. Go to your /etc/ssl director
2. Generate self-signed key:
       - openssl req \
       - key 131.104.49.102.key \
       - new \
       - x509 -days 365 -out 131.104.49.102.crt

### View certificate:
```
openssl x509 -text -noout -in 131.104.49.102.crt
```

### View private key:
```
openssl rsa -check -in 131.104.49.102.key
```

## Resources used:
- https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-debian-10
- https://www.nginx.com/resources/wiki/start/?_bt=541137080527&_bk=&_bm=&_bn=g&_bg=125748574545&gclid=CjwKCAiApfeQBhAUEiwA7K_UH2p_JFq-szDxAg5ma1UbNCMZDzoNDd5DFah1Y4L4QZFOgcE2yQSL8RoCYxUQAvD_BwE
- https://www.digitalocean.com/community/tutorials/openssl-essentials-working-with-ssl-certificates-private-keys-and-csrs
- https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04