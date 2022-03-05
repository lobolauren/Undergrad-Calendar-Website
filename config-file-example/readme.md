# config README
currently the site shows as "Not Secure" due to the ssl certificate being self signed

# config file
add the config file to /etc/nginx/sites-available
it will autamatically also be added to /etc/nginx/sites-enabled

NOTE: When making changes to the config files for nginx, remember to reload nginx for the changes to take effect using this command: `sudo systemctl restart nginx`

# logs
you can find the access log at /var/log/nginx/access.log
you can find the error log at /var/log/nginx/error.log

In order to read them, you will have to use the following command:
`sudo vi` followed by which log you would like to read.

# add the ssl certificate and key
go to your /etc/ssl director

generate self-signed key:
openssl req \
       -key 131.104.49.102.key \
       -new \
       -x509 -days 365 -out 131.104.49.102.crt

View certificate:
openssl x509 -text -noout -in 131.104.49.102.crt

View private key:
openssl rsa -check -in 131.104.49.102.key






# Resources Used
https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-debian-10
https://www.nginx.com/resources/wiki/start/?_bt=541137080527&_bk=&_bm=&_bn=g&_bg=125748574545&gclid=CjwKCAiApfeQBhAUEiwA7K_UH2p_JFq-szDxAg5ma1UbNCMZDzoNDd5DFah1Y4L4QZFOgcE2yQSL8RoCYxUQAvD_BwE
https://www.digitalocean.com/community/tutorials/openssl-essentials-working-with-ssl-certificates-private-keys-and-csrs
