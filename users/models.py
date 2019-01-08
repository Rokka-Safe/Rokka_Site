import time
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/apprenant/Bureau/Rokka_Site/rokka.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255)) # encryption !! RGPD !!!
    activated = db.Column(db.Boolean())
    activated_at = db.Column(db.String(20))

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.activated = True
        self.activated_at = time.strftime("%Y-%m-%d")

    def __repr__(self):
        return "User {first_name} {last_name}".format(
            first_name=self.first_name,
            last_name=self.last
        )


class APIKey(db.Model):
    __tablename__   = 'api_keys'
    id              = db.Column(db.Integer, primary_key=True)
    tmp_code        = db.Column(db.Integer)
    key             = db.Column(db.String(25))
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'))
    user            = db.relationship('User', backref=db.backref('users.id', lazy='joined'))

    def __init__(self, tmp_code, key, user_id):
        self.tmp_code = tmp_code
        self.key = key
        self.user_id = user_id

    def __repr__(self):
        return "You have the following key : {key}".format(
            key=self.key
        )
