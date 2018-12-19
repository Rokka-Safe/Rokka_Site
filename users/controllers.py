from flask import Blueprint, render_template

main = Blueprint('users', __name__)


@users.route('/users', methods=['GET', 'POST'])
def user():
    return render_template('home.html')
