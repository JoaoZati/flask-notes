from flask import Blueprint, render_template, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note
from website import db

views = Blueprint('views', __name__, )


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note must have at least one character', category='error')
            return render_template('home.html', user=current_user)
        new_note = Note(data=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Note created with success', category='success')

    return render_template('home.html', user=current_user)
