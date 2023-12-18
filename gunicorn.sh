#!/bin/bash

pyenv activate chat-app-server


cd /var/lib/jenkins/workspace/chat-app-server

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

echo "Migration completed"

sudo cp -rf gunicorn.socket /etc/systemd/system/
sudo cp -rf gunicorn.service /etc/systemd/system/

echo "$USER"
echo "$PWD"



sudo systemctl daemon-reload
sudo systemctl start gunicorn

echo "Gunicorn has started."

sudo systemctl enable gunicorn

echo "Gunicorn has been enabled."

sudo systemctl restart gunicorn


sudo systemctl status gunicorn


