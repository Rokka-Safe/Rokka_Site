#!flask/bin/python
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from users.models import db
from users.models import User

import requests

app = Flask(__name__)
db.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////home/apprenant/Bureau/Rokka_Site/rokka.db"
db = SQLAlchemy(app)

#
#
# Webapp routes
#
#

@app.route('/')
def home():
    print(requests)
    return render_template('home.html')


@app.route('/user', methods=['POST'])
def create_user():
    new_user = User(
        first_name=request.form["first_name"],
        last_name=request.form["last_name"],
        email=request.form["email"],
        password=request.form["password"]
    )
    db.session.add(new_user)
    db.session.commit()
    return 'You have successfully created your account !'


@app.route('/user/<int:user_id>', methods=['GET', 'DELETE'])
def me(user_id):
    if request.method == 'GET':
        current_user = User.query.filter_by(id=user_id).first_or_404()
        return render_template('profile.html', current_user=current_user)
    elif request.method == 'DELETE':
        return 'Account removed'

#
#
# Raspberry routes
#
#