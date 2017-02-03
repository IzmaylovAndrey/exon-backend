from flask_restful import request, Api, Resource
from app import db, models


class UserList(Resource):
    def get(self):
        return models.User.query.all()

    def post(self):
        return 200
