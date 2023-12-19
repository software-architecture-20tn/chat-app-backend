#!/bin/bash

sudo cp -rf jenkins-scripts/app.conf /etc/nginx/sites-available/chat-app.nguyenvanloc.name.vn
sudo chmod 710 /var/lib/jenkins/workspace/chat-app-backend

sudo nginx -t

sudo systemctl start nginx
sudo systemctl enable nginx

echo "Nginx has been started"

sudo systemctl status nginx
