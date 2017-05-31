from flask import url_for, redirect, request, flash
from flask_login import login_user
from passlib.hash import sha256_crypt


def log_in(user, password):
    try:
        if user is None:
            flash('Invalid Credentials.')
            return redirect(request.url)
        else:
            pwd = user.password
            if sha256_crypt.verify(password, pwd):
                login_user(user)
                flash('Hello, ' + user.username + '!')

                return redirect(request.url or url_for('homepage'))
            else:
                flash('Invalid Credentials.')
                return redirect(request.url)

    except Exception as e:
        return redirect(url_for("login_page", error=(str(e))))
