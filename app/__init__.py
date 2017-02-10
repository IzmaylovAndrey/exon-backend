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

from app.resources import User, UserEmails, UserList, TariffList, Login, Logout
# Routes for api
api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(UserEmails, '/users/<int:id>/emails', endpoint='user_emails')
api.add_resource(User, '/users/<int:id>', endpoint='user')
api.add_resource(TariffList, '/tariffs', endpoint='tariffs')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
