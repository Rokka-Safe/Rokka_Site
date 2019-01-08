from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import User, APIKey, db
import random

load_dotenv()

app = Flask(__name__)
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////home/apprenant/Bureau/Rokka_Site/rokka.db"
db = SQLAlchemy(app)


class UserController:

    @staticmethod
    def signin(req):
        return req

    @staticmethod
    def create(req):
        new_user = User(
            first_name=req["first_name"],
            last_name=req["last_name"],
            email=req["email"],
            password=req["password"]
        )
        db.session.add(new_user)
        db.session.commit()
        return 'You have successfully created your account !'

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

class BadgeController:

    @staticmethod
    def register_badge(key, user_id):
        random_tmp = str(random.randint(0, 9))
        for x in range(5):
            random_tmp += str(random.randint(0, 9))
        new_badge = APIKey(
            tmp_code=random_tmp,
            key=key,
            user_id=user_id
        )
        db.session.add(new_badge)
        db.session.commit()
        return 'You have successfully registered your badge !'

    @staticmethod
    def clear_badge(key, user_id):
        # TODO : the val remowhole
        current_badge = APIKey.query.filter_by(key=key, user_id=user_id).first_or_404()
        db.session.delete(current_badge)
        db.session.commit()
        return "You've removed your badge"
