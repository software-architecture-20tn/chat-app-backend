#!/bin/bash

cp -rf app.conf /etc/nginx/sites-available/app
chmod 710 /var/lib/jenkins/workspace/chat-app-backend

ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled
nginx -t

systemctl start nginx
systemctl enable nginx

echo "Nginx has been started"

systemctl status nginx
