from flask import Flask, render_template, request,session, redirect, url_for, escape
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/apprenant/Documents/Rokka_Site/rokka.db'
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.route('/testform')
def hello_world():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
     #return '<h1>{}</h1>'.format(request.form['username'])
     user = User(username=request.form['username'], email=request.form['email'])
     db.session.add(user)
     db.session.commit()
     return redirect(url_for('success'))

@app.route('/success')
def success():
   return 'logged in successfully'