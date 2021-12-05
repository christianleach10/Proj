from datetime import datetime

import sqlalchemy
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from app import app, db
# from app.forms import LoginForm, RegistrationForm, EditProfileForm, \
#    EmptyForm, PostForm, ResetPasswordRequestForm, ResetPasswordForm
# from app.models import User, Post
# from app.email import send_password_reset_email
from app.forms import LoginForm, RegistrationForm, NewReviewForm, TrailReviewForm, Search
from app.models import User, Trail, Review, TrailToReview


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = Search()
    form.difficulty.choices = ["", "Easy", "Moderate", "Hard"]
    form.length.choices = ["", "Short, 1-3 miles", "Moderate, 3-6 miles", "Long, 6-10 miles"]
    db_query = Trail.query
    if form.validate_on_submit():

        if form.trailname.data is not None:
            db_query = db_query \
                .filter(Trail.name.contains(form.trailname.data))
        if form.difficulty.data is not "":
            db_query = db_query \
                .filter_by(difficulty=form.difficulty.data)
        if form.length.data is not "":
            if form.length.data == "Short, 1-3":
                db_query = db_query \
                    .filter_by(Trail.distance <= 3)
            if form.length.data == "Moderate, 3-6 miles":
                db_query = db_query \
                    .filter_by(Trail.distance <= 6 and Trail.distance > 3)
            if form.length.data == "Long, 6-10 miles":
                db_query = db_query \
                    .filter_by(Trail.distance > 6)


        trails = db_query.all()
        return render_template("trails.html", user="Search Results", trails=trails)

    user = 'The Holy Trail'
    posts = [
        {
            'body': 'Find a Trail Today!'
        },

    ]
    return render_template('index.html', title='Home', user=user, posts=posts, form=form)


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
    user = "List of Trails!"
    trails = Trail.query.filter().all()
    return render_template('trails.html', user=user, trails=trails)


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
    t1 = Trail(name="Robert Treeman", distance="6 Miles", difficulty="Hard", location="14850",description="Ready for your next hike or bike ride? Explore one of 2 easy hiking trails in Robert H. Treman State Park that are great for the whole family. Looking for a more strenuous hike? We've got you covered, with trails ranging from 9 to 3,510 feet in elevation gain. Whatever you have planned for the day, you can find the perfect trail for your next trip to Robert H. Treman State Park.")
    t2 = Trail(name="Ithaca Falls", distance="1.2 Miles", difficulty="Easy", location="14850", description="Ithaca Falls Trail is a 0.2 mile heavily trafficked out and back trail located near Ithaca, New York that features a waterfall and is good for all skill levels. The trail is primarily used for walking and nature trips and is accessible year-round. Dogs are also able to use this trail but must be kept on leash.")
    t3 = Trail(name="Botanical Gardens", distance="1.1 Miles", difficulty="Easy", location="14850", description="Cascadilla Falls (9 falls) is a 1.1 mile heavily trafficked out and back trail located near Ithaca, New York that features a waterfall and is rated as moderate. The trail is primarily used for hiking, walking, nature trips, and bird watching and is accessible year-round. Dogs are also able to use this trail but must be kept on leash.")
    t4 = Trail(name="Taughannock", distance="4 Miles", difficulty="Moderate", location="14850", description="Ready for your next hike or bike ride? Explore one of 3 easy hiking trails in Taughannock Falls State Park that are great for the whole family. Looking for a more strenuous hike? We've got you covered, with trails ranging from 82 to 593 feet in elevation gain. Whatever you have planned for the day, you can find the perfect trail for your next trip to Taughannock Falls State Park")
    t5 = Trail(name="Buttermilk Falls", distance="3 Miles", difficulty="Moderate", location="14850", description="Buttermilk Falls: Gorge and Rim Trail Loop is a 1.6 mile heavily trafficked loop trail located near Ithaca, New York that features a waterfall and is rated as moderate. The trail is primarily used for hiking, walking, camping, and nature trips and is best used from May until September. Dogs are also able to use this trail but must be kept on leash.")
    db.session.add_all([t1, t2, t3, t4, t5])
    db.session.commit()

    u1 = User(username="KosmoKramer", email="KKramer@ithaca.edu")
    u2 = User(username="JerrySeinfeld", email="JSeinfeld@ithaca.edu")
    u3 = User(username="ElaineBennis", email="EBennis@ithaca.edu")
    u4 = User(username="Newman", email="Newman@ithaca.edu")
    u5 = User(username="GeorgeCostanza", email="GCostanza@ithaca.edu")
    db.session.add_all([u1, u2, u3, u4, u5])
    db.session.commit()

    r1 = Review(userID=u1.id, rating=5, description="It was very good")
    r2 = Review(userID=u2.id, rating=3, description="It was very mid")
    r3 = Review(userID=u3.id, rating=1, description="It Stunk")
    r4 = Review(userID=u4.id, rating=4, description="Beatufil,too long tho")
    r5 = Review(userID=u5.id, rating=2, description="Treacherous, good views")
    db.session.add_all([r1, r2, r3, r4, r5])
    db.session.commit()

    t2r1 = TrailToReview(trail_id=t1.id, review_id=r5.id)
    t2r2 = TrailToReview(trail_id=t3.id, review_id=r4.id)
    t2r3 = TrailToReview(trail_id=t4.id, review_id=r3.id)
    t2r4 = TrailToReview(trail_id=t2.id, review_id=r2.id)
    t2r5 = TrailToReview(trail_id=t5.id, review_id=r1.id)
    db.session.add_all([t2r1, t2r2, t2r3, t2r4, t2r5])
    db.session.commit()

    return render_template('base.html', title='home')


@app.route('/trailAndReview/<name>')
def trail(name):
    trail = Trail.query.filter(Trail.name == name).first()
    return render_template('trailAndReview.html', trail=trail)


@app.route('/newreview', methods=['GET', 'POST'])
def newreview():
    form = NewReviewForm()
    form.trails.choices = [(t.id, t.name) for t in Trail.query.all()]
    form.rating.choices = [0,1,2,3,4,5]
    try:
        if form.validate_on_submit():
            review = Review(rating=form.rating.data,
                            description=form.description.data,
                            userID=current_user.id)
            db.session.add(review)
            db.session.commit()
            for trail_id in form.trails.data:
                t2r = TrailToReview(trail_id=trail_id, review_id=review.id)
                db.session.add(t2r)
            db.session.commit()

            flash('Congratulations, you left a new review!')
            return redirect(url_for('trails'))
    except sqlalchemy.exc.IntegrityError:
        flash("You already reviewed this trail.")
    return render_template('newreview.html', title='New Review', form=form)


@app.route('/trailreview/<name>', methods=['GET', 'POST'])
def trailreview(name):
    trail = Trail.query.filter(Trail.name == name).first()
    form = TrailReviewForm()
    form.rating.choices = [0, 1, 2, 3, 4, 5]
    try:
        if form.validate_on_submit():
            review = Review(rating=form.rating.data,
                            description=form.description.data,
                            userID=current_user.id)
            db.session.add(review)
            db.session.commit()

            t2r = TrailToReview(trail_id=trail.id, review_id=review.id)
            db.session.add(t2r)
            db.session.commit()

            flash('Congratulations, you left a new review!')
            return redirect(url_for('trails'))
    except sqlalchemy.exc.IntegrityError:
        flash("You already reviewed this trail.")
    return render_template('TrailReviewForm.html', title='New Review', form=form, name=trail.name)
@app.route('/myreviews')
def myreviews():
    title = "My Reviews"
    reviews = []
    review = Review.query.filter_by(id=current_user.id).all()
    reviews.append(review)
    return render_template('myreviews.html', title=title, reviews=reviews)
