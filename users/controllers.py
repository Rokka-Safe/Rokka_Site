from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import login_user, current_user
from flask_sqlalchemy import SQLAlchemy
from time import gmtime, strftime
from dotenv import load_dotenv
from sqlalchemy import delete
from models import User, APIKey, Logs, db
import sqlite3
import random
import json
import os

load_dotenv()

app = Flask(__name__)
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'rokka'


class UserController:

    @staticmethod
    def signin(req):
        user = User.query.filter_by(email=req.email.data).first()
        if user is None or not user.check_password(req.password.data):
            flash('Invalid email or password')
            return redirect(url_for('signin'))
        login_user(user, remember=req.remember_me.data)
        return login_user

    @staticmethod
    def create(req):
        user = User(first_name=req.first_name.data, last_name=req.last_name.data, email=req.email.data)
        user.set_password(req.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User registered')

    @staticmethod
    def delete(user_id):
        current_user = User.query.filter_by(id=user_id).first_or_404()
        db.session.delete(current_user)
        db.session.commit()
        return 'Account removed'

    @staticmethod
    def show(user_id):
        current_user = User.query.filter_by(id=user_id).first_or_404()
        return render_template('profile.html', current_user=current_user)

    @staticmethod
    def edit(req):
        current_user.first_name = req.first_name.data
        current_user.last_name = req.last_name.data
        current_user.set_password(req.password.data)
        flash('Your changes have been saved')


class BadgeController:

    def __init__(self):
        pass

    @staticmethod
    def register_badge(req):
        safe = APIKey(name=req.name, tmp_code=BadgeController.generate_random(), key=req.pid, user_id=current_user.id)
        db.session.add(safe)
        db.session.commit()
        flash('Your ROKKA has been saved')


    @staticmethod
    def authenticate(data, user_id):
        d = json.loads(data)
        conn = sqlite3.connect("rokka.db")
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE id = {id};".format(id=user_id))
        current_user = cur.fetchall()
        cur.execute("SELECT key, tmp_code FROM api_keys WHERE key = '{key}';".format(key=d["key"]))
        current_safe = cur.fetchall()

        try:
            if d['key'] == current_safe[0][0] and user_id == current_user[0][0] and d["code"] == current_safe[0][1]:
                return True
        except IndexError:
            return False


    @staticmethod
    def write_json_file(key, user_id):
        path = './static/data/{key}_{user_id}.json'.format(key=key, user_id=user_id)
        data = {
            "key": key,
            "key_confirmation": "",
            "user_id": str(user_id),
            "created_at": strftime("%Y-%m-%d", gmtime())
        }
        with open(path, 'w') as f:
            f.write(json.dumps(data))

        return True if len(data['key_confirmation']) > 0 else False

    @staticmethod
    def generate_random():
        random_tmp = str(random.randint(0, 9))
        for x in range(5):
            random_tmp += str(random.randint(0, 9))
        return random_tmp


def clear_badge(key, user_id):
    current_badge = APIKey.query.filter_by(key=key, user_id=user_id).first_or_404()

    # TODO: introduce double check before removal
    print(current_badge)
    db.execute(delete('api_keys').where())
    db.session.commit()

    return "You've removed your badge"


class LogsController:

    @staticmethod
    def log_event(safe_id, status):
        new_log = Logs(
            status=status,
            created_at=strftime("%Y-%m-%d", gmtime()),
            safe_id=safe_id
        )
        db.session.add(new_log)
        db.session.commit()
        return 'ok'
