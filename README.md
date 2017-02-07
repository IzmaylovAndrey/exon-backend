# Deployment

_All things should be done in project dir_

## Install [PostgreSQL](https://www.postgresql.org/)
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib python-psycopg2

sudo -u postgres createuser --interactive //there you should input <username>
sudo -u postgres createdb exon
sudo -u postgres psql << "ALTER USER <username> with encrypted password <your_password>;"

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

## Deactivate environment
```bash
deactivate
```

