#!flask/bin/python
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from users.models import db

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


@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'GET':
        return 'foo'
    elif request.method == 'POST':
        return 'bar'


@app.route('/me/{user_id}', methods=['GET', 'DELETE'])
def me(user_id):
    if request.method == 'GET':
        print(user_id)
        return render_template('me.html')
    elif request.method == 'DELETE':
        return 'delete me'

#
#
# Raspberry routes
#
#