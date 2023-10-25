# Notice
After merging codes into `main` branch, please make sure to do the instructions in [this section](#instructions-for-running-backend-on-development-server).
# Instructions for running backend on local
## Environment variables
First, please check [this file](https://drive.google.com/file/d/1mNtVXMRDJOgGnZNoWOGOx0ZdWK9qY9pp/view), with some modifications:
- Change its name to `.env`
- If you perform changes about values in this `.env` file, please make sure to change corresponding values in `docker-compose.yml` file as well.
> :warning: **Do not use the development database as `DATABASE_HOST` when running in local**

## Prequisites:
In this project, we use `pyenv` to manage virtual environments, please make sure that you have `pip`, `pyenv`, and `pyenv-virtualenv` installed. If not, please follow the instructions on below pages:
- [pip](https://pip.pypa.io/en/stable/installation/)
- [pyenv](https://github.com/pyenv/pyenv#installation)
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

After installation, you may need to add some lines to your `.bashrc` or `.zshrc` file. Check [this section](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv) for more details.

## Virtual environment & dependencies setup
### Setup virtual environment
```bash
pip install -r requirements/local.txt
pyenv virtualenv-delete --force chat-app-backend
pyenv install 3.11 --skip-existing
pyenv virtualenv 3.11 chat-app-backend
pyenv local chat-app-backend
pyenv activate chat-app-backend
```

**Note (OPTIONAL)**: If you face some issues with the last command while running with Pyenv >= 2.0 (Error message: `Failed to activate virtualenv`), please try to add these lines to your `.profile` file:
```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
eval "$(pyenv init -)"
```
### Setup dependencies
Before doing this, please make sure the virtual environment is activated.
You can check this by running:
```
pyenv versions
```
And if the result is something like this:
```
  system
  3.11.5
  3.11.5/envs/chat-app-backend
* chat-app-backend --> /Users/vanloc1808/.pyenv/versions/3.11.5/envs/chat-app-backend (set by /Users/vanloc1808/GitHub/chat-app-backend/.python-version)
```
Notice the asterisk `*` in front of `chat-app-backend`, which means that the virtual environment is activated.

Then, run the following commands:
```bash
pip install -r requirements/local.txt  # yes, we run this command again, as now we are in the virtual environment
pip install -r requirements/development.txt
```

**Note (OPTIONAL)**: If you get stuck with some libraries like `psycopg2`, please try to install `libpq-dev` and `python3-dev` packages by running:
```bash
sudo apt install libpq-dev python3-dev
```

Done, the virtual environment and dependencies are set up.

## Running project
Now, to verify the setup, run:
```bash
inv django.run
```
This is an [invoke](https://www.pyinvoke.org/) command. You can take a look at its documentation to understand more about `invoke`. In short, it helps us to run commands in a more convenient way.

## Other invokes
All `invoke` commands used in project can be found in `tasks.py` file. You can run `inv --list` to see all available commands.
### About Django
Every time we make change on our models, please ensure to make migrations of the, do this by running:
```bash
inv django.makemigrations
```
It is equivalent to `python manage.py makemigrations` command.

To apply the migrations, run:
```bash
inv django.migrate
```
It is equivalent to `python manage.py migrate` command.

For running the server, run:
```bash
inv django.run
```
It is equivalent to `python manage.py runserver_plus` command.
### About Docker
Every time we run Django server, the docker containers are automatically
up (or built if there has not yet), so we do not need to run docker commands.
However, if we want to run docker commands, we can use `invoke` as well.
For upping the containers, run:
```bash
inv docker.up
```
It is equivalent to `docker-compose up` command.
For stopping the containers, run:
```bash
inv docker.stop
```
It is equivalent to `docker-compose stop` command.

# Instructions for running backend on development server
We have a VPS that hosts our development server. Every time you merge codes into `main` branch, please make sure to do the below:
```bash
ssh root@15.235.186.83
```
Contact me for the password.
Then,
```bash
cd /home/projects/chat-app-backend/
git pull
```
Please make sure that the pulling process is successful. If not, please contact me.
Then, run this command to see the processes that are using port 8000:
```bash
lsof -i:8000 -t
```
There will be 2 process IDs (PIDs) returned. Kill them by running:
```bash
kill <PID>
```
Then, verify the killing process by running this command again:
```bash
lsof -i:8000 -t
```
Then, start the server again by running:
```bash
nohup ./run.sh &
```
Please notice the ampersand `&` at the end of the command. It is used to run the command in background, so that we can close the SSH connection without stopping the server.
Then, verify the running process by running:
```bash
lsof -i:8000 -t
```
There will be 2 new PIDs returned. If not, please contact me.
Then, close the SSH connection by running:
```bash
exit
```

## Dependencies addition
When you added a dependency, for example, `numpy`, add it to `production.in` file, then run
```
inv pip.compile-dependencies
```
