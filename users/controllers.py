from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib
from flask_login import login_user, current_user
from models import User, APIKey, Logs, db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete, update
from time import gmtime, strftime
from dotenv import load_dotenv
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
            return False
        login_user(user, remember=req.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return next_page

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

    @staticmethod
    def register_badge(req):
        safe = APIKey(name=req.name.data, tmp_code=BadgeController.generate_random(), key=req.pid.data, user_id=current_user.id)
        db.session.add(safe)
        db.session.commit()
        flash('Your ROKKA has been saved')

    @staticmethod
    def VerifyBadge(key, user_id):
        current_badge = APIKey.query.filter_by(key=key, user_id=user_id).first()
        if current_badge is None:
            return jsonify(
                status=False,
            )
        else:
            return jsonify(
                status=True,
            )

    @staticmethod
    def authenticate(data):
        d = json.loads(data)
        conn = sqlite3.connect("rokka.db")
        cur = conn.cursor()
        cur.execute("SELECT key, tmp_code, user_id FROM api_keys WHERE key = '{key}' LIMIT 1;".format(key=d["key"]))
        current_safe = cur.fetchall()
        cur.close()

        try:
            if d['key'] == current_safe[0][0] and current_safe[0][2] >= 0 and str(d["code"]) == str(current_safe[0][1]):
                LogsController.log_event('success : openned the safe', current_safe[0][0])
                return True
        except IndexError:
            return False
        except:
            return False

    @staticmethod
    def reset_code(safe):
        code = BadgeController.generate_random()
        safe.tmp_code = code
        user = User.query.filter_by(id=safe.user_id).first_or_404()
        db.current_session = db.session.object_session(safe)
        db.current_session.add(safe)
        db.current_session.commit()

        MailerController.send_mail(code,  str(safe.name), email=str(user.email))
        LogsController.log_event('success : reset code', key=safe.key)

        return 'Success'

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

    @staticmethod
    def clear_badge(key, user_id):
        current_badge = APIKey.query.filter_by(key=key, user_id=user_id).first_or_404()

        current_badge.delete().where(current_badge.key == key)
        db.session.commit()

        return "You've removed your badge"


class LogsController:

    @staticmethod
    def log_event(status, key=None, safe_id=None):
        if safe_id is None:
            new_log = Logs(
                status=status,
                created_at=strftime("%Y-%m-%d", gmtime()),
                safe_id=key
            )
        else:
            new_log = Logs(
                status=status,
                created_at=strftime("%Y-%m-%d", gmtime()),
                safe_id=safe_id
            )
        db.session.add(new_log)
        db.session.commit()
        return 'ok'


class MailerController:

    @staticmethod
    def send_mail(code, safe, email='dummyuseerr@gmail.com'):
        msg = MIMEMultipart()
        msg['From'] = 'Rokka team'
        msg['To'] = email
        msg['Subject'] = 'Your code has been changed'
        message = 'Your code for {safe} has been changed ! Here is the new one : {code}'.format(
            code=code,
            safe=safe
        )
        msg.attach(MIMEText(message))
        mailserver = smtplib.SMTP('smtp.gmail.com', 587)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login('rokkacontact@gmail.com', os.getenv("GMAIL_PASS"))
        mailserver.sendmail('rokkacontact@gmail.com', 'dummyuseerr@gmail.com', msg.as_string())
        mailserver.quit()
        return 'ok'
