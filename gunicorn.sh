#!/bin/bash

cd /var/lib/jenkins/workspace/chat-app-backend

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput

echo "Migration completed"
cp -rf gunicorn.socket /etc/systemd/system/
cp -rf gunicorn.service /etc/systemd/system/

echo "$USER"
echo "$PWD"

systemctl daemon-reload
systemctl start gunicorn

echo "Gunicorn has started."

systemctl enable gunicorn

echo "Gunicorn has been enabled."

systemctl restart gunicorn

systemctl status gunicorn


