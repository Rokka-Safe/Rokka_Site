#!flask/bin/python
from flask import Flask, request, render_template

import requests

app = Flask(__name__)

# Webapp routes


@app.route('/')
def home():
    print(requests)
    return render_template('home.html')

@app.route('/me')
def me():
    return render_template('me.html')


# Raspberry routes