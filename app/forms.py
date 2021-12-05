from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')



class NewReviewForm(FlaskForm):
    trails = SelectField('Trail Name:', choices=[], validators=[DataRequired()])
    rating = SelectField('Rating:', choices=[], validators=[DataRequired()])
    description = StringField('Description:', validators=[DataRequired()])
    submit = SubmitField('Enter review')

class TrailReviewForm(FlaskForm):
    rating = SelectField('Rating:', choices=[], validators=[DataRequired()])
    description = StringField('Description:', validators=[DataRequired()])
    submit = SubmitField('Enter review')

class Search(FlaskForm):
    trailname = StringField('Trail Name:')
    difficulty = SelectField('Select Difficulty:', choices=[])
    length = SelectField('Select Length:', choices=[])
    submit = SubmitField('Enter search')
