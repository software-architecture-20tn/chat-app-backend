#!/bin/bash

cd /var/lib/jenkins/workspace/chat-app-backend

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput

echo "Migration completed"
sudo cp -rf jenkins-scripts/gunicorn.socket /etc/systemd/system/
sudo cp -rf jenkins-scripts/gunicorn.service /etc/systemd/system/

echo "$USER"
echo "$PWD"

sudo systemctl daemon-reload
sudo systemctl start gunicorn

echo "Gunicorn has started."

sudo systemctl enable gunicorn

echo "Gunicorn has been enabled."

sudo systemctl restart gunicorn

sudo systemctl status gunicorn


