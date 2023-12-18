#!/bin/bash

pyenv activate chat-app-server


cd /var/lib/jenkins/workspace/chat-app-server

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

echo "Migration completed"


