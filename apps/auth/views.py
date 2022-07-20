from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from database import db
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__, template_folder="templates/auth")


@auth.route("/signin")
def signin():
    return render_template('signin.html')


@auth.route("/signin", methods=['POST'])
def signin_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Falsche Anmeldeinformationen, bitte versuchen Sie es erneut!')
        return redirect(url_for('auth.signin'))  # if the user doesn't exist or password is wrong, reload the page

    login_user(user, remember=remember)

    return redirect(url_for('main.index'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('username')
    password = request.form.get('password')

    # check if user exists
    user = User.query.filter_by(email=email).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email ist bereits vergeben!')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.signin'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.app_errorhandler(404)
def page_not_found():
    return render_template('layouts/404.html'), 404
