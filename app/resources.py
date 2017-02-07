from app import api, models, db
from flask_restful import Resource, reqparse, fields, marshal_with

user_parser = reqparse.RequestParser()
user_parser.add_argument('id', type=int)
user_parser.add_argument('username')
user_parser.add_argument('password')
user_parser.add_argument('first_name')
user_parser.add_argument('last_name')
user_parser.add_argument('phone')
user_parser.add_argument('company')
user_parser.add_argument('address')

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
    'last_name': fields.String,
    'phone': fields.String,
    'company': fields.String,
    'address': fields.String,
    'mails': fields.List(fields.Nested(mail_fields)),
    'tariff': fields.Nested(tariff_fields, allow_null=True),
}

user_list_fields = {
    fields.List(fields.Nested(user_fields)),
}

mail_list_fields = {
    fields.List(fields.Nested(mail_fields))
}

tariff_list = {
    fields.List(fields.Nested(tariff_fields))
}


class UserList(Resource):
    @marshal_with(user_list_fields, envelope='resource')
    def get(self):
        return models.User.query.all()

    @marshal_with(user_list_fields, envelope='resource')
    def post(self):
        return 201


class User(Resource):
    @marshal_with(user_fields, envelope='resource')
    def get(self, pk):
        return models.User.query.get(pk=pk)

    def put(self, pk):
        user = models.User.query.get(pk=pk)
        return 202

    def delete(self, pk):
        return 204


class TariffList(Resource):
    @marshal_with(tariff_list, envelope='resource')
    def get(self):
        return models.Tariff.query.all()

    def post(self):
        tariff = models.Tariff()
        db.session.add(tariff)
        return 201


class UserEmails(Resource):
    @marshal_with(mail_fields, envelope='resource')
    def get(self, user_id):
        user = models.User.query.get(pk=user_id)
        return user.user_emails

    @marshal_with(mail_fields, envelope='resource')
    def post(self, user_id):
        return 200


class Login(Resource):
    def get(self):
        return "Make a POST request"

    # TODO: login mechanism
    def post(self):
        return 200


class Logout(Resource):
    def post(self):
        return 200

api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<user_id>')
api.add_resource(UserEmails, '/users/<user_id/emails>')
