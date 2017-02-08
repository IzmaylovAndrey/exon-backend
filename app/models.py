from app import app
from app import db
from flask_user import UserMixin, SQLAlchemyAdapter, UserManager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False, default='')

    is_enabled = db.Column(db.Boolean, default=True)

    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(50))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(15))

    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))
    user_emails = db.relationship('UserMail')
    tariff = db.Column(db.ForeignKey('tariff.id'))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(32), nullable=False, unique=True)


class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


class UserMail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    email = db.Column(db.String(100), unique=True)
    is_primary = db.Column(db.Boolean, default=False)
    confirmed_at = db.Column(db.DateTime())


# TODO: change description to list of parameters
class Tariff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    price = db.Column(db.Float, default=0.0)
    description = db.Column(db.String(255))

db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
user_manager = UserManager(db_adapter, app)     # Initialize Flask-User
