from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    reviews = db.relationship('Review', backref = 'author', lazy = 'dynamic')
    history = db.relationship('History', backref = 'user', lazy = 'dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    rating = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pair_id = db.Column(db.Integer, db.ForeignKey('pair.id'))

    def __repr__(self):
        return '<Review {} {}>'.format(self.body, self.user_id)


class Pair(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    wine = db.Column(db.String(140))
    food = db.Column(db.String(140))
    reviews = db.relationship('Review', backref = 'pairing', lazy = 'dynamic')
    history = db.relationship('History', backref = 'pairing', lazy = 'dynamic')

    def __repr__(self):
        return '<Pair {} + {}>'.format(self.wine, self.food)


class History(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pair_id = db.Column(db.Integer, db.ForeignKey('pair.id'))
    time = db.Column(db.DateTime, index = True, default = datetime.utcnow)

    def __repr__(self):
        return '<History {} {} {}>'.format(self.id, self.time, self.user_id)
