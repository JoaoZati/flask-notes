from flask import Blueprint, render_template, request, flash, redirect, url_for

from website import db

from website.models import User, Note

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__, )


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password1')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))

        flash('Wrong email or password', category='error')

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were successfully Logged out', 'success')
    return redirect(url_for('auth.login'))


@auth.route('/sing-up', methods=['GET', 'POST'])
def sing_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(firstname) < 3:
            flash('First name must be greater than 2 characters', category='error')
        elif password1 != password2:
            flash('Passwords must be equal', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 6 characters', category='error')
        else:
            new_user = User(email=email, first_name=firstname,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Sing up successfully', category='success',)
            return redirect( url_for('views.home'))

    return render_template('sing_up.html')
