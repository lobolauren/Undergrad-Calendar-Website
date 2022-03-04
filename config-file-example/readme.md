# config README
currently the site shows as "Not Secure" due to the ssl certificate being self signed

# config file
add the config file to /etc/nginx/sites-available
it will autamatically also be added to /etc/nginx/sites-enabled

# logs
you can find the access log at /var/log/nginx/access.log
you can find the error log at /var/log/nginx/error.log

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
