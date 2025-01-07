#!/bin/bash

cd /var/lib/jenkins/workspace/chat-app-backend
uv venv --python 3.11 --prompt chat --seed
source .venv/bin/activate


pip3 install -r requirements/development.txt

python manage.py test

if [ -d "logs" ]
then
    echo "Log folder exists."
else
    mkdir logs
    touch logs/error.log logs/access.log
fi
