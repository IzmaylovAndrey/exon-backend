## System requirements

- Python 3.5
- PostgreSQL 9.5
- Python-Psycopg2
- Virtualenv


## Deployment

**All things should be done in project dir**

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

### Deactivate environment
```bash
deactivate
```

