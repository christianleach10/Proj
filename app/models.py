from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)
    description = db.Column(db.String(256))
    t2rs = db.relationship('TrailToReview', backref='review', lazy='dynamic')

    def __repr__(self):
        return '{} was rated {} because {}'.format(self.userID, self.rating, self.description)

class Trail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    distance = db.Column(db.String(64), index=True)
    difficulty = db.Column(db.String(64), index=True)
    location = db.Column(db.String(64), index=True)
    description = db.Column(db.String(64), index=True)
    t2rs = db.relationship('TrailToReview', backref='trail', lazy='dynamic')




class TrailToReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trail_id = db.Column(db.Integer, db.ForeignKey('trail.id'))
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    reviews = db.relationship('Review', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
