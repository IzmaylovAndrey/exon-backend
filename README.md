# Deployment

_All things should be done in project dir_

1. Install [PostgreSQL](https://www.postgresql.org/)

```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

2. Install [virtualenv](https://virtualenv.pypa.io/en/stable/)

```bash
pip install virtualenv
```

3. Create virtual environment

```bash
virtualenv env
```

4. Activate virtual environment

```bash
source env/bin/activate
```

5. Install all required python packages

```bash
pip install -r requirements.txt
```

