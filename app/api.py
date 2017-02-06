from app import api
from flask_restful import Resource, reqparse, fields, marshal_with

user_parser = reqparse.RequestParser()
user_parser.add_argument('id', type=int)
user_parser.add_argument('username')
user_parser.add_argument('password')

tariff_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'price': fields.Float,
    'description': fields.String
}

mail_fields = {
    'email': fields.String,
    'is_primary': fields.Boolean,
    'confirmed_at': fields.DateTime,
}

# TODO: nested list with emails
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'first_name': fields.String,
    'second_name': fields.String,
    'phone': fields.String,
    'company': fields.String,
    'address': fields.String,
    'mails': fields.List(fields.Nested(mail_fields)),
    'tariff': fields.Nested(tariff_fields, allow_null=True),
}

user_list_fields = {
    fields.List(fields.Nested(user_fields)),
}


class UserList(Resource):
    @marshal_with(user_list_fields, envelope='resource')
    def get(self):
        return

    def post(self):
        return 200


class User(Resource):
    @marshal_with(user_fields, envelope='resource')
    def get(self, pk):
        return pk

api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<user_id>')
