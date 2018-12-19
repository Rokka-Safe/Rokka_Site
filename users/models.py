from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255)) # encryption !! RGPD !!!
    activated = db.Column(db.Boolean())
    activated_at = db.Column(db.Datetime())

    def __init__(self, id, first_name, last_name, email, password, activated, activated_at):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.activated = activated
        self.activated_at = activated_at

    def __repr__(self):
        return "User {first_name} {last_name}".format(
            first_name=self.first_name,
            last_name=self.last
        )


class API_Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tmp_code = db.Column(db.Integer)
    key = db.Column(db.String(15))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('users', lazy='joined'))

    def __init__(self, id, tmp_code, key, user_id):
        self.id = id
        self.tmp_code = tmp_code
        self.key = key
        self.user_id = user_id

    def __repr__(self):
        return "You have the following key : {key}".format(
            key=self.key
        )
