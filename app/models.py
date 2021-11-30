from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.String(16))
    description = db.Column(db.String(256))
    u2rs = db.relationship('UserToReview', backref='review', lazy='dynamic')
    t2rs = db.relationship('TrailToReview', backref='review', lazy='dynamic')

    def __repr__(self):
        return '{} was rated {} because {}'.format(self.name, self.rating, self.description)
class Trail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    distance = db.Column(db.String(64), index=True)
    difficulty = db.Column(db.String(64), index=True)
    location = db.Column(db.String(64), index=True)
    t2rs = db.relationship('TrailToReview', backref='trail', lazy='dynamic')


class UserToReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'))


class TrailToReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trail_id = db.Column(db.Integer, db.ForeignKey('trail.id'))
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
