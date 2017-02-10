from flask_restful import Resource, reqparse, fields, marshal_with, http_status_message
from flask_user.passwords import hash_password
from flask_login import logout_user, login_user
# TODO: add roles
from app.decorators import login_required

from app import models, db
from app.models import user_manager

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
    'emails': fields.Nested(mail_fields),
    'tariff_id': fields.Integer,
}

# mail_list_fields = {
#     'emails': fields.List(fields.Nested(mail_fields)),
# }
# tariff_list = {
#     'tariffs': fields.List(fields.Nested(tariff_fields)),
# }


def get_default_tariff():
    tariff = models.Tariff.query.filter(models.Tariff.name == 'default').first_or_404()
    return tariff


def get_user_role():
    role = models.Role.query.filter(models.Role.name == 'user').first_or_404()
    return role


class User(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
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

    @login_required
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
                if k is 'password':
                    setattr(user, k, hash_password(user_manager, v))
                setattr(user, k, v)
        user.tariff_id = get_default_tariff().id
        db.session.add(user)

        mail = models.UserMail()
        mail.user_id = user.id
        mail.email = user.username
        mail.is_primary = True
        # TODO: new email confirmation
        # email.confirmed_at = time()
        db.session.add(mail)

        user_role = models.UserRoles()
        user_role.role_id = get_user_role().id
        user_role.user_id = user.id
        db.session.add(user_role)

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

    @marshal_with(tariff_fields)
    def get(self, id):
        return models.Tariff.query.filter(models.Tariff.id == id).first_or_404()

    # admin_role
    @marshal_with(tariff_fields)
    def put(self, id):
        tariff = models.Tariff.query.filter(models.Tariff.id == id).first_or_404()
        args = self.parser.parse_args()
        for k, v in args.items():
            if v is not None:
                setattr(tariff, k, v)
        db.session.commit()
        return models.Tariff.query.get(id), 202

    # admin_role
    @marshal_with(tariff_fields)
    def delete(self, id):
        tariff = models.Tariff.query.filter(models.Tariff.id == id).first_or_404()
        db.session.delete(tariff)
        db.session.commit()
        return http_status_message(204)


class UserEmails(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type=str, required=True, help='No email provided')
        self.parser.add_argument('is_primary', type=bool, default=False)
        super(UserEmails, self).__init__()

    # or admin_role
    @marshal_with(mail_fields)
    @login_required
    def get(self, id):
        user = models.User.query.filter(models.User.id == id).first_or_404()
        return user.user_emails

    # or admin_role
    # TODO: new email confirmation
    @login_required
    @marshal_with(mail_fields)
    def post(self, id):
        user = models.User.query.filter(models.User.id == id).first_or_404()
        args = self.parser.parse_args()
        email = models.UserMail()

        for k, v in args.items():
            setattr(email, k, v)
        email.user_id = user.id
        # email.confirmed_at = time()

        db.session.add(email)
        db.session.commit()
        return user.user_emails, 201


# TODO: create resource to get, edit, delete emails
# TODO: email confirmation
class Mail(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type=str)
        self.parser.add_argument('is_primary', type=bool)
        super(Mail, self).__init__()

    @login_required
    @marshal_with(tariff_fields)
    def get(self, id):
        return models.UserMail.query.filter(models.UserMail.id == id).first_or_404()

    # or admin_role
    @login_required
    @marshal_with(tariff_fields)
    def put(self, id):
        tariff = models.UserMail.query.filter(models.UserMail.id == id).first_or_404()
        args = self.parser.parse_args()
        for k, v in args.items():
            if v is not None:
                setattr(tariff, k, v)
        db.session.commit()
        return models.UserMail.query.get(id), 202

    # admin_role
    @marshal_with(tariff_fields)
    def delete(self, id):
        tariff = models.UserMail.query.filter(models.Tariff.id == id).first_or_404()
        db.session.delete(tariff)
        db.session.commit()
        return http_status_message(204)


class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True)
        self.parser.add_argument('password', type=str, required=True)
        self.parser.add_argument('remember', type=bool, default=False)
        self.parser.add_argument('force', type=bool, default=False)
        super(Login, self).__init__()

    def post(self):
        args = self.parser.parse_args()
        user = models.User.query.filter(models.User.username == args['username']).first_or_404()
        if models.user_manager.verify_password(password=args['password'], user=user):
            login_user(user, remember=args['remember'], force=args['force'])
        return http_status_message(200)


class Logout(Resource):
    @login_required
    def post(self, id):
        logout_user()
        return http_status_message(200)


class ChangeUsername(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('new_username', type=str)
        super(ChangeUsername, self).__init__()

    @login_required
    @marshal_with(user_fields)
    def post(self, id):
        user = models.User.query.filter(models.User.id == id).first_or_404()
        args = self.parser.parse_args()
        args = args['args']
        user.username = args['username']
        return user, 202


class ChangePassword(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('new_password', type=str)
        super(ChangePassword, self).__init__()

    @login_required
    @marshal_with(user_fields)
    def post(self, id):
        user = models.User.query.filter(models.User.id == id).first_or_404()
        args = self.parser.parse_args()
        args = args['args']
        user.password = hash_password(models.user_manager, password=args['new_password'])
        return user, 202
