from flask import Flask
# from flask_login import LoginManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
# lm = LoginManager()
# lm.init_app(app)
api = Api(app)

from app.resources import User, UserList, UserEmails
# Routes for api
api.add_resource(UserList, '/users')
api.add_resource(UserEmails, '/users/<user_id>/emails')
api.add_resource(User, '/users/<user_id>')
