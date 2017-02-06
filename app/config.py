import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/exon'
FLASK_DEBUG = True

# TODO: Config mailing
# MAIL_USERNAME = 'email@example.com'
# MAIL_PASSWORD = 'password'
# MAIL_DEFAULT_SENDER = '“Sender” <noreply@example.com>’'
# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_PORT = 465
# MAIL_USE_SSL = True
# MAIL_USE_TLS = False

# Flask-RESTful section
BUNDLE_ERRORS = True
