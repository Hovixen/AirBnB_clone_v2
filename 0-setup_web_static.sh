#!/usr/bin/env bash
# Script sets up web severs for the deployment of web_static

apt-get -y update
apt-get -y install nginx

mkdir -p /data/web_static/{releases/test,shared}

echo "Holberton School" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test /data/web_static/current

chown -R ubuntu:ubuntu /data

REDIRECT="https://github.com/Hovixen/"

ERR_MSG="Ceci n'est pas une page"

CONFIG="server {
        listen 80;
        server_name _;
        root /var/www/html;
        index index.nginx-debian.html;

	location = /hbnb_static {
	alias /data/web_static/current;
	index index.html index.htm;
	}

        location = /redirect_me {
                return 301 $REDIRECT;
        }

        error_page 404 /404_error;
        location = /404_error {
                internal;
                return 404 \"$ERR_MSG\n\";
        }
}"
echo "$CONFIG" > /etc/nginx/sites-available/default
service nginx restart
