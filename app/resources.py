from time import time

from flask_restful import Resource, reqparse, fields, marshal_with, http_status_message
from flask_user.passwords import hash_password
from flask_login import logout_user, login_user
# TODO: add roles and auth decorators
# from flask_user.decorators import login_required, roles_required

from app import models, db

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

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'phone': fields.String,
    'company': fields.String,
    'address': fields.String,
    'emails': fields.List(fields.Nested(mail_fields)),
    'tariff': fields.Nested(tariff_fields, allow_null=True),
}

# mail_list_fields = {
#     'emails': fields.List(fields.Nested(mail_fields)),
# }
# tariff_list = {
#     'tariffs': fields.List(fields.Nested(tariff_fields)),
# }


def get_default_tariff():
    tariff = models.Tariff.query().filter(models.Tariff.name == 'default').first()
    return tariff


class User(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        # self.parser.add_argument('id', type=int)
        self.parser.add_argument('first_name', type=str)
        self.parser.add_argument('last_name', type=str)
        self.parser.add_argument('phone', type=str)
        self.parser.add_argument('company', type=str)
        self.parser.add_argument('address', type=str)
        super(User, self).__init__()

    @marshal_with(user_fields)
    def get(self, id):
        user = models.User.query.filter(models.User.id == id).first_or_404()
        return user

    # auth_req
    @marshal_with(user_fields)
    def put(self, id):
        user = models.User.query.filter(models.User.id == id).first_or_404()
        args = self.parser.parse_args()
        for k, v in args.items():
            if v is not None:
                setattr(user, k, v)
        db.session.commit()
        return user, 202

    # admin_role
    @marshal_with(user_fields)
    def delete(self, id):
        user = models.User.query.filter(models.User.id == id).first_or_404()
        db.session.delete(user)
        db.session.commit()
        return http_status_message(204)


class UserList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, help='No username provided')
        self.parser.add_argument('password', type=str, required=True, help='No password provided')
        self.parser.add_argument('first_name', type=str)
        self.parser.add_argument('last_name', type=str)
        self.parser.add_argument('phone', type=str)
        self.parser.add_argument('company', type=str)
        self.parser.add_argument('address', type=str)
        super(UserList, self).__init__()

    # admin_role (?)
    @marshal_with(user_fields)
    def get(self):
        return models.User.query.all()

    # registration endpoint
    @marshal_with(user_fields)
    def post(self):
        args = self.parser.parse_args()
        user = models.User()
        for k, v in args.items():
            if v is not None:
                setattr(user, k, v)
        user.tariff = get_default_tariff()
        db.session.add(user)
        db.session.commit()

        email = models.UserMail()
        email.user_id = user.id
        email.email = user.username
        email.is_primary = True
        # TODO: new email confirmation
        email.confirmed_at = time()
        db.session.add(email)
        db.session.commit()
        return models.User.query.all(), 201


class TariffList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help='No tariff name provided')
        self.parser.add_argument('price', type=float, required=True, help='No tariff price provided')
        self.parser.add_argument('description', type=str)
        super(TariffList, self).__init__()

    @marshal_with(tariff_fields, envelope='tariffs')
    def get(self):
        return models.Tariff.query.all()

    # admin_role
    @marshal_with(tariff_fields)
    def post(self):
        tariff = models.Tariff()
        args = self.parser.parse_args()
        for k, v in args.items():
            if v is not None:
                setattr(tariff, k, v)
        db.session.add(tariff)
        db.commit()
        return models.Tariff.query.all(), 201


class Tariff(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help='No tariff name provided')
        self.parser.add_argument('price', type=float, required=True, help='No tariff price provided')
        self.parser.add_argument('description', type=str)
        super(Tariff, self).__init__()

    def get(self, id):
        return models.Tariff.query.get(id)

    # admin_role
    def put(self, id):
        return models.Tariff.query.get(id), 202

    # admin_role
    def delete(self, id):
        return 204


class UserEmails(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type=str, required=True, help='No email provided')
        self.parser.add_argument('is_primary', type=bool)
        super(UserEmails, self).__init__()

    # auth_req or admin_role
    @marshal_with(mail_fields, envelope='emails')
    def get(self, id):
        user = models.User.query.filter(models.User.id == id).first_or_404()
        return user.user_emails

    # auth_req or admin_role
    # TODO: new email confirmation
    @marshal_with(mail_fields, envelope='emails')
    def post(self, id):
        user = models.User.query.filter(models.User.id == id).first_or_404()
        args = self.parser.parse_args()
        email = models.UserMail()

        for k, v in args.items():
            setattr(email, k, v)
        email.user_id = user.id
        # TODO: new email confirmation
        email.confirmed_at = time()

        db.session.add(email)
        db.session.commit()
        return user.user_emails, 201


class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True)
        self.parser.add_argument('password', type=str, required=True)
        super(Login, self).__init__()

    def post(self):
        args = self.parser.parse_args()
        args = args['args']
        user = models.User.query.filter(models.User.username == args['username']).first_or_404()
        if user.password == hash_password(models.user_manager, args['password']):
            login_user(user)
        return 200


class Logout(Resource):
    # auth_req
    def post(self, id):
        logout_user()
        return 200


class ChangeUsername(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('new_username', type=str)
        super(ChangeUsername, self).__init__()

    # auth_req
    @marshal_with(user_fields)
    def post(self, id):
        user = models.User.query.filter(models.User.id == id).first_or_404()
        args = self.parser.parse_args()
        args = args['args']
        user.username = args['username']
        return user


class ChangePassword(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('new_password', type=str)
        super(ChangePassword, self).__init__()

    # auth_req
    @marshal_with(user_fields)
    def post(self, id):
        user = models.User.query.filter(models.User.id == id).first_or_404()
        args = self.parser.parse_args()
        args = args['args']
        user.password = hash_password(models.user_manager, password=args['new_password'])
        return user
