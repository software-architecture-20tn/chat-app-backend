# Install virtual env
```bash
pip install -r requirements/local.txt
pyenv virtualenv-delete --force app-name-server
pyenv install 3.11 --skip-existing
pyenv virtualenv 3.11 app-name-server
pyenv local app-name-server
pyenv activate app-name-server
```
