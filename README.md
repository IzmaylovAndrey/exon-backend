## System requirements
- Python 3.5
- PostgreSQL 9.5
- Python-Psycopg2
- Virtualenv

## Project structure
- /app - app code dir
- /docs - docs dir
- /migrations
- config.py - config file, should be improved
- manage.py - file for making migrations and db upgrade. 
Docs on [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
- requirements.txt - file with description of necessary python packages for installation from pip
- run.py - file for running application

## Deployment

**All things should be done in project dir(besides postgres)**

### Install python3

```bash
sudo apt-get update
sudo apt-get install python3
```

### Install [PostgreSQL](https://www.postgresql.org/) and Psycopg
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib python-psycopg2

sudo -u postgres createuser --interactive //there you should input 'username'
sudo -u postgres createdb exon
sudo -u postgres psql << "ALTER USER 'username' with encrypted password 'your_new_password';"
```

After all this things restart postgres.service

### Install virtualenv

```bash
sudo pip install virtualenv
```

### Create virtual environment
```bash
virtualenv env
```
### Activate virtual environment
```bash
source env/bin/activate
```
### Install all required python packages
```bash
pip install -r requirements.txt
```

### To deactivate environment
```bash
deactivate
```

### Upgrade db to last migration

```bash
python manage.py db init
python manage.py db upgrage
```
