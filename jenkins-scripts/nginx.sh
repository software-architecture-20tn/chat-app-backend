#!/bin/bash

# sudo cp -rf jenkins-scripts/app.conf /etc/nginx/sites-available/chat-app.nguyenvanloc.name.vn
sudo chmod -R 777 /var/lib/jenkins/workspace/chat-app-backend

sudo nginx -t

sudo systemctl restart nginx
sudo systemctl enable nginx

echo "Nginx has been started"

sudo systemctl status nginx
