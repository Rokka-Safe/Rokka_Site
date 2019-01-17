import time
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'signin'
app.config['SECRET_KEY'] = 'rokka'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), index=True)
    last_name = db.Column(db.String(255), index=True)
    email = db.Column(db.String(255), index=True, unique=True)
    password = db.Column(db.String(255))  # encryption !! RGPD !!!
    activated = db.Column(db.Boolean())
    activated_at = db.Column(db.String(20))

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.activated = True
        self.activated_at = time.strftime("%Y-%m-%d")

    def __repr__(self):
        return "User {first_name} {last_name}".format(
            first_name=self.first_name,
            last_name=self.last_name
        )

    def safes(self):
        return APIKey.query.filter_by(user_id=self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class APIKey(db.Model):
    __tablename__ = 'api_keys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    tmp_code = db.Column(db.Integer)
    key = db.Column(db.String(25), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('users.id', lazy='joined'))

    def __init__(self, name, tmp_code, key, user_id):
        self.name = name
        self.tmp_code = tmp_code
        self.key = key
        self.user_id = user_id

    def __repr__(self):
        return "{key}".format(key=self.key)

    def logs(self):
        return Logs.query.filter_by(safe_id=self.id)


class Logs(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(25))
    created_at = db.Column(db.String(255))
    safe_id = db.Column(db.Integer, db.ForeignKey('api_keys.id'))
    safe = db.relationship('APIKey', backref=db.backref('api_keys.id', lazy='joined'))

    def __init__(self, status, created_at, safe_id):
        self.status = status
        self.created_at = created_at
        self.safe_id = safe_id

    def __repr__(self):
        return "{safe_id}".format(safe_id=self.safe_id)
