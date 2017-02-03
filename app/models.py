from app import db, app
from flask_user import UserMixin, SQLAlchemyAdapter, UserManager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(50))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(15))

    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))
    user_emails = db.relationship('UserMail')


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(32), nullable=False, unique=True)


class UserRoles(db.Model):
    user_id = db.Column(db.ForeignKey('user.id', ON_DELETE='CASCADE'))
    role_id = db.Column(db.ForeignKey('role.id', ON_DELETE='CASCADE'))


class UserMail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id', ON_DELETE='CASCADE'))
    email = db.Column(db.String(100), unique=True)
    is_primary = db.Column(db.Boolean, default=False)
    confirmed_at = db.Column(db.DateTime())


db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
user_manager = UserManager(db_adapter, app)     # Initialize Flask-User

