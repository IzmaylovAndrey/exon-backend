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

from app.resources import User, UserEmails, UserList, TariffList, Login, Logout, ChangeUsername, ChangePassword, \
                          Tariff, Mail

# Routes for api
api.add_resource(UserList, '/api/users', endpoint='users')

api.add_resource(Login, '/api/login', endpoint='login')
api.add_resource(Logout, '/api/logout', endpoint='logout')
api.add_resource(ChangePassword, '/api/change_password', endpoint='change_password')
api.add_resource(ChangeUsername, '/api/change_username', endpoint='change_username')
api.add_resource(User, '/api/users/<int:id>', endpoint='user')
api.add_resource(UserEmails, '/api/users/<int:id>/emails', endpoint='user_emails')

api.add_resource(TariffList, '/api/tariffs', endpoint='tariffs')

api.add_resource(Tariff, '/api/tariff/<int:id>', endpoint='tariff')
