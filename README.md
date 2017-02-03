# Deployment

_All things should be done in project dir_

## Install [PostgreSQL](https://www.postgresql.org/)
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```
## Install [virtualenv](https://virtualenv.pypa.io/en/stable/)
```bash
pip install virtualenv
```
## Create virtual environment
```bash
virtualenv env
```
## Activate virtual environment
```bash
source env/bin/activate
```
## Install all required python packages
```bash
pip install -r requirements.txt
```

