#!flask/bin/python
from flask import Flask, request, render_template
from users.controllers import UserController, BadgeController, LogsController
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from users.models import db
import os

load_dotenv()

app = Flask(__name__, static_url_path="/static")
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)

#
#
# Webapp routes
#
#


@app.route('/signin', methods=['POST'])
def signin():
    UserController.signin(request.form)
    return


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/user', methods=['POST'])
def create_user():
    try:
        return UserController.create(request.form)
    except:
        return render_template('404.html')


@app.route('/user/<int:user_id>', methods=['GET', 'DELETE'])
def me(user_id):
    if request.method == 'GET':
        return UserController.show(user_id)
    elif request.method == 'DELETE':
        try:
            return UserController.delete(user_id)
        except:
            return render_template('404.html')


@app.route('/tutorial/<int:step>', methods=['GET'])
def get_tutorial(step):
    return render_template('tutorial.html', step=step)

#
#
# Raspberry routes
#
#


@app.route('/api/badge/<key>/<int:user_id>', methods=['GET', 'DELETE'])
def badge(key, user_id):
    return "123"
    # return BadgeController.clear_badge(key, user_id) if request.method == 'DELETE' else BadgeController.register_badge(key, user_id)


@app.route('/api/log', methods=["POST"])
def log_event():
    data = request.get_json()
    safe_id = str(data["safe_id"])
    status = data["status"]
    return LogsController.log_event(safe_id, status) if request.method == 'POST' else render_template('404')
