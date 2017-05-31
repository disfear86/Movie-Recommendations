from app import app
from app.models import Base, User
from create_db import engine

from flask import render_template, redirect, url_for, request, flash, jsonify, g
from flask import session as ls
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.orm import sessionmaker
from app import forms
from app.forms import LoginForm, RegistrationForm
from app.oauth import FacebookOAuth, GoogleOAuth
from app.auth import log_in
from passlib.hash import sha256_crypt


Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    if not current_user.is_anonymous:
        return redirect(url_for('homepage'))
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user_submit = request.form['email']
        password = request.form['password']
        user = session.query(User).filter_by(email=user_submit).first()
        return log_in(user, password)
    return render_template('login.html', form=form)


@app.route('/register/', methods=['GET', 'POST'])
def registration_page():
    if not current_user.is_anonymous:
        return redirect(url_for('homepage'))
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)

        user_data = session.query(User).filter_by(username=username).first()
        user_email = session.query(User).filter_by(email=email).first()

        if user_data is not None:
            flash('Username not available.')
            return redirect(url_for('registration_page', form=form))
        elif user_email is not None:
            flash('Email is already in use.')
            return redirect(url_for('registration_page', form=form))
        else:
            new_user = User(username=username, email=email, password=password)
            session.add(new_user)
            session.commit()

            login_user(new_user)
            flash('Registration Successful.')

            return redirect(url_for('homepage'))
    return render_template('register.html', form=form)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/user/')
@login_required
def user_main():
    user = current_user
    return render_template('user.html', user=user)


@app.route('/search/', methods=['GET', 'POST'])
def search():
    if request.method == "POST":

        search_data = request.form['search']
        if not search_data:
            data = 'No data entered.'
            return redirect(url_for('search', data=data))

        restaurants = []
        menus = []

        search_rests = session.query(Restaurant).all()
        for entry in search_rests:
            if entry.name.lower().startswith(search_data):
                restaurants.append(entry)

        search_menu = session.query(MenuItem).all()
        for entry in search_menu:
            if entry.name.startswith(search_data):
                rest_name = session.query(Restaurant).filter_by(id=entry.restaurant_id).one()
                menus.append((entry, rest_name))

        if restaurants == []:
            rests_data = 'No restaurants found.'
        else:
            rests_data = restaurants
        if menus == []:
            menu_data = 'No menu entries found.'
        else:
            menu_data = menus

        return render_template('search.html', rests_data=rests_data,
                                menu_data=menu_data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html")
