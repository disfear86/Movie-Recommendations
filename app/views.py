from app import app
from app.models import Base, User
from create_db import engine

from flask import render_template, redirect, url_for, request, flash, g
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.orm import sessionmaker
from app.forms import LoginForm, RegistrationForm
from app.auth import log_in
from passlib.hash import sha256_crypt
from recommend import find_similar
import pandas as pd
import numpy as np
from celery import Celery
import gc
from imdb import IMDb


Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

movie_ratings = pd.read_csv('app/movie_ratings.csv')

ratings_table = movie_ratings.pivot_table(index=['user_id'],
                                          columns=['movie_id'],
                                          values='rating')

'''
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task(bind=True)
def get_info_task(self, title, ia):
    s_result = ia.search_movie(title)[0].movieID
    result = ia.get_movie(s_result)
    return result
'''


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
    _user = movie_ratings['user_id'] == user.id
    user_movies = movie_ratings[_user]
    user_movies.sort_values(['title'], inplace=True)
    z = zip(user_movies['movie_id'], user_movies['title'], user_movies['rating'])
    return render_template('user.html', data=user_movies, z=z)


@app.route('/user/<int:movie_id>')
@login_required
def movie_page(movie_id):
    user = current_user
    _movie = movie_ratings[movie_ratings['movie_id'] == movie_id]
    movie = _movie[_movie['user_id'] == user.id]
    title = str(movie['title'].values[0][:-6])

    # ia = IMDb()
    # res = get_info_task(title, ia)

    similar = find_similar(ratings_table, movie_id)
    similar_ids = pd.Series(similar.index.values.tolist())

    movie_group = movie_ratings.drop_duplicates(subset=['movie_id'], keep='first', inplace=False)
    movie_list = [movie_group.iloc[i] for i in similar_ids]

    gc.collect()
    return render_template('movie.html', data=movie, title=title,
                           movie_list=movie_list)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html")
