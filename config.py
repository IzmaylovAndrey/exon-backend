import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql:///exon'
SQLALCHEMY_TRACK_MODIFICATIONS = True
FLASK_DEBUG = True
SECRET_KEY = 'i_wanna_know_it'

# TODO: Configure mailing
# MAIL_USERNAME = 'email@example.com'
# MAIL_PASSWORD = 'password'
# MAIL_DEFAULT_SENDER = 'Sender <noreply@example.com>'
# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_PORT = 465
# MAIL_USE_SSL = True
# MAIL_USE_TLS = False

# Flask-RESTful section
BUNDLE_ERRORS = True

# Flask-User settings
USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password
USER_ENABLE_CHANGE_USERNAME = False  # Allow users to change their username
USER_ENABLE_CONFIRM_EMAIL = True  # Force users to confirm their email
USER_ENABLE_FORGOT_PASSWORD = True  # Allow users to reset their passwords
USER_ENABLE_EMAIL = True  # Register with Email
USER_ENABLE_REGISTRATION = True  # Allow new users to register
USER_ENABLE_RETYPE_PASSWORD = True  # Prompt for `retype password` in:
USER_ENABLE_USERNAME = False  # Register and Login with username
# USER_AFTER_LOGIN_ENDPOINT = 'user_page'
# USER_AFTER_LOGOUT_ENDPOINT = 'home_page'
