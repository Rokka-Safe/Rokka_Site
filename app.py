#!flask/bin/python
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from users.models import db
from users.models import User
from users.controllers import UserController

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
    try:
        UserController.create(request.form)
        return 'You have successfully created your account !'
    except:
        return render_template('404.html')


@app.route('/user/<int:user_id>', methods=['GET', 'DELETE'])
def me(user_id):
    if request.method == 'GET':
        return UserController.show(user_id)
    elif request.method == 'DELETE':
        try:
            UserController.delete(user_id)
            return 'Account removed'
        except:
            return render_template('404.html')

#
#
# Raspberry routes
#
#
