# from flask import Blueprint, render_template
# main = Blueprint('users', __name__)
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from models import User, db

app = Flask(__name__)
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////home/apprenant/Bureau/Rokka_Site/rokka.db"
db = SQLAlchemy(app)


class UserController:

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

    @staticmethod
    def delete(user_id):
        current_user = User.query.filter_by(id=user_id).first_or_404()
        db.session.delete(current_user)
        db.session.commit()

    @staticmethod
    def show(user_id):
        current_user = User.query.filter_by(id=user_id).first_or_404()
        return render_template('profile.html', current_user=current_user)
