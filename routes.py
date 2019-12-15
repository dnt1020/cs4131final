from flask import render_template, flash, redirect, url_for, request
import requests
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, RequestForm, ReviewForm
from flask_login import current_user, login_user
from app.models import User, Pair, History, Review
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse

# WHEN LOGGING OUT AND THEN LOGGING BACK IN AN ERROR HAPPENS

API_KEY = "3495005704df46f9a4bad5b39efc4023"

#for record last visit time:
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    form = RequestForm()
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
    return render_template('index.html', title='Home', reviews=reviews, form=form)


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



    pairings = History.query.filter(History.user_id == user.id)

    reviews = Review.query.filter(Review.user_id == user.id)

    for i in pairings:
        print(i.user)

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

## DOES API LOOKUP
@app.route('/pairs', methods=['POST','GET'])
def apiLookup():
    form = RequestForm()
    if form.validate_on_submit():
        wine = form.wine.data
        food = form.food.data
    else:
        print("nonvalid")
        return render_template("index.html", form=form)

    if wine != "":
        url = "https://api.spoonacular.com/food/wine/dishes?wine=" + wine  + "&apiKey=" + API_KEY
        response = requests.get(url)
        foodpairings = list()
        for x in response.json()[u'pairings']:
            foodpairings.append(x.encode("ascii"))
            print(x.encode("ascii"))
        return render_template("pairings.html", wine = wine, foodpairings = foodpairings)
    else:
        url = "https://api.spoonacular.com/food/wine/pairing?food=" + food + "&apiKey=" + API_KEY
        response = requests.get(url)
        winepairings = list()
        for x in response.json()[u'pairedWines']:
            winepairings.append(x.encode("ascii"))
            print(x.encode("ascii"))
        return render_template("pairings.html", food = food, winepairings = winepairings)

## CALLED FROM JS AFTER USER PRESSES A PAIR
@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    wine = request.args.get('wine', 1)
    food = request.args.get('food', 1)

    ##Check if pairing already exists
    checkEntry = Pair.query.filter(Pair.wine == wine, Pair.food == food)
    if (len(checkEntry.all()) > 0):
        ## if already exists
        pair = checkEntry[0]
    else:
        ## get wine and food from something
        pair = Pair(wine = wine, food = food)
        db.session.add(pair)
        db.session.commit()
        ## IDK WHAT THIS DOES
        print('added pairing??')

    ## FIX FAVORITE THING ValidationError
    #add pairing to History
    u = User.query.get(current_user.id)
    print("id: " + u.username)
    #change favorites to be variable?
    history = History(pairing = pair, user = u, favorite = True)
    db.session.add(history)
    db.session.commit()
    print('added history??')

    return "success"

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

    pairings = History.query.filter(History.user_id == current_user.id)

    return render_template('pair.html', pair=pair, reviews=reviews, form = form)
