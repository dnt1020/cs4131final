from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, RequestForm, ReviewForm
from flask_login import current_user, login_user
from app.models import User, Pair, History, Review
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse

# WHEN LOGGING OUT AND THEN LOGGING BACK IN AN ERROR HAPPENS


#for record last visit time:
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    reviews = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', reviews=reviews)


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

##SOMETHING HERE MESSED UP??

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


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    pairings = User.query.join(User.history).filter(user.id == id)

    reviews = Review.query.filter(Review.user_id == user.id)

    return render_template('user.html', user=user, reviews=reviews, history = pairings)


#For recording last visit time
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


## FOR USER TO EDIT A PROF
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/requests', methods=['GET', 'POST'])
@login_required
def requests():
    ## THIS ISN'T A REAL FORM YET
    form = RequestForm()
    if form.validate_on_submit():

        ##Check if pairing already exists
        checkEntry = Pair.query.filter(Pair.wine == form.wine.data, Pair.food == form.food.data)
        if (len(checkEntry.all()) > 0):
            ## if already exists
            pair = checkEntry[0]
        else:
            ## get wine and food from something
            pair = Pair(wine = form.wine.data, food = form.food.data)
            db.session.add(pair)
            db.session.commit()
            ## IDK WHAT THIS DOES
            flash('added pairing??')

        ## FIX FAVORITE THING ValidationError
        #add pairing to History
        u = User.query.get(current_user.id)
        print("id: " + u.username)
        history = History(pairing = pair, user = u, favorite = form.fave.data)
        db.session.add(history)
        db.session.commit()
        flash('added history??')

    return render_template("requests.html", form=form)


#### HANDLE IF PAIRING ID DOESN'T EXIST

@app.route('/pairing/<id>', methods=['GET', 'POST'])
@login_required
def pairing(id):

    ## CHECK TO MAKE SURE WAS GIVEN THE PAIRING TO BE ABLE TO MAKE A REVIEW
    form = ReviewForm()
    ## NEED TO FIGURE OUT HOW TO GET THE PAIRING ID
    if form.validate_on_submit():
        review = Review(body = form.review.data, rating = form.rate.data, author = current_user, pairing = Pair.query.get(id))
        db.session.add(review)
        db.session.commit()
        flash('Review updated')
        return redirect(url_for('index'))

    pair = Pair.query.filter_by(id = id).first_or_404()

    reviews = Review.query.filter(Review.pair_id == id)

    return render_template('pair.html', pair=pair, reviews=reviews, form = form)
