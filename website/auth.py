from flask import Blueprint, render_template, flash, redirect, url_for, request
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.profile'))
            flash('Username or password was incorrect.', category='error')
    return render_template('login.html',headlinks=render_template('headlinks.html'))

@auth.route('logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/signup", methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('fname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        new_user = User(email=email,fname=first_name, password=generate_password_hash(password1))
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists, please login', category='error')
            return render_template('signup.html',headlinks=render_template('headlinks.html'))
        print(new_user.email)
        #return render_template('signup.html',headlinks=render_template('headlinks.html'))

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash('Account created!', category='success')

        return redirect(url_for('views.home'))

    return render_template('signup.html',headlinks=render_template('headlinks.html'))