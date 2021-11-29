from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse


from app import app, db
#from app.forms import LoginForm, RegistrationForm, EditProfileForm, \
#    EmptyForm, PostForm, ResetPasswordRequestForm, ResetPasswordForm
#from app.models import User, Post
#from app.email import send_password_reset_email
from app.forms import LoginForm, RegistrationForm
from app.models import User, Trail


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'The Holy Trail'}
    posts = [
        {

            'body': 'Find a Trail Today!'
        },



    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/trails')
def trails():

    user = 'List of Trails'
    trails = trails.query.filter().all()
    return render_template('trails.html',user=user, trails=trails)

@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()

@app.route('/populate_db')
def populate_db():
    reset_db()
    t1 = Trail(name="Robert Treeman", distance="6 Miles", difficulty="Hard", location ="14850" )
    t2 = Trail(name="Gorge Trail", distance="1.2 Miles", difficulty="Moderate", location ="14850" )
    t3 = Trail(name="Botanical Gardens", distance="2.5 Miles", difficulty="Easy", location ="14850" )
    t4 = Trail(name="Taughannock", distance="4 Miles", difficulty="Modereate", location ="14850" )
    t5 = Trail(name="Buttermilk Falls", distance="3 Miles", difficulty="Easy", location ="14850" )
    db.session.add_all([t1, t2, t3, t4, t5])
    db.session.commit()
    return render_template('base.html', title='home')


