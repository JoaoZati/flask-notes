from flask import Blueprint, render_template, request, flash, redirect, url_for

from website import db
from website.models import User, Note

from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__, )


@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    return render_template('login.html')


@auth.route('/logout')
def logout():
    return render_template('home.html')


@auth.route('/sing-up', methods=['GET', 'POST'])
def sing_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
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
            flash('Sing up successfully', category='success',)
            return redirect( url_for('views.home'))

    return render_template('sing_up.html')
