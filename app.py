#!flask/bin/python
import os
import json
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse
from users.controllers import UserController, BadgeController, LogsController
from users.forms import LoginForm, RegisterForm, SafeForm, EditProfileForm
from users.models import db, User, APIKey

load_dotenv()

app = Flask(__name__, static_url_path="/static")
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SECRET_KEY'] = 'rokka'
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'signin'


#
#
# Webapp routes
#
#


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        UserController.signin(form)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('signin.html', title='Sign In', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        UserController.create(form)
        return redirect(url_for('signin'))
    return render_template('signup.html', title='Register', form=form)


@app.route('/')
def home():
    return render_template('home.html', current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


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


@app.route('/user/<email>/profile/', methods=['GET', 'POST'])
@login_required
def user_profile(email):
    user = User.query.filter_by(email=email).first_or_404()
    form = EditProfileForm()
    if form.validate_on_submit():
        UserController.edit(form)
        return redirect(url_for('user_profile', email=current_user.email))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
    return render_template('profile.html', title='Edit Profile', form=form, user=user)


@app.route('/user/<email>/safes')
@login_required
def safes(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        return redirect(url_for('home'))
    all_safes = current_user.safes().all()
    return render_template('my_rokka.html', title='My ROKKA', safes=all_safes)


@app.route('/user/add_safe')
@login_required
def add_safe():
    form = SafeForm
    if form.validate_on_submit():
        r = requests.post('192.168.1.221:5000/registerBagde/', json.dumps(form), )
        req_data = r.json()
        response = req_data['status']
        if response == 'success':
            BadgeController.register_badge(form)
            return redirect(url_for('home'))
    return render_template('tutorial_02.html', title='Add ROKKA', form=form)


@app.route('/tutorial/<int:step>', methods=['GET'])
@login_required
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


@app.route('/api/badge/check', methods=['POST'])
def check_badge():
    data = request.get_json()
    return 'success' if BadgeController.authenticate(json.dumps(data)) else 'fail'


@app.route('/api/log', methods=["POST"])
def log_event():
    data = request.get_json()
    safe_id = str(data["safe_id"])
    status = data["status"]
    return LogsController.log_event(safe_id, status) if request.method == 'POST' else render_template('404')
