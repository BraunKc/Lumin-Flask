from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from config import *
from User import User


# WTFORMS
from login_form import *
from registration_form import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home_page():
    return render_template('home.html')

# REGISTER LOGIN LOGOUT

@app.route('/registration', methods=['GET', 'POST'])
def registration_page():
    if current_user.is_authenticated:
        return redirect(url_for('notes_page'))

    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit:
        email = form.email.data
        username = form.username.data
        psw = generate_password_hash(form.psw.data)

        user = User(username=username, email=email, password=psw)

        try:
            db.session.add(user)
            db.session.commit()

            login_user(user)

            return redirect(url_for('notes_page'))
        except:
            return 'Произошла ошибка при сохранении данных в базу данных'
    return render_template('authentication.html', title='Lumin', action='register', RegisterForm=RegisterForm(), LoginForm=LoginForm())

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('notes_page'))

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit:
        email = form.email.data
        psw = form.psw.data

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, psw):
            login_user(user)
            return redirect(url_for('notes_page'))
        return 'Неверные данные', 401
    return render_template('authentication.html', title='Lumin', action='login', RegisterForm=RegisterForm(), LoginForm=LoginForm())

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_page'))

# NOTES

# all notes
@app.route('/notes')
def notes_page():
    return render_template('notes.html', title='Lumin | Notes')

# create note (no visual)
@app.route('/notes/create', methods=['GET', 'POST'])
def create_note():
    return redirect(url_for('note_page(note_id)'))

# note page, user can edit it
@app.route('/notes/<note_id>', methods=['GET', 'POST'])
def note_page(note_id):
    return render_template('note.html', title='')

# delete note (no visual)
@app.route('/notes/<note_id>/delete', methods=['GET', 'POST'])
def delete_note(note_id):
    return redirect(url_for('notes_page'))

# USER

# account page (information about user), can edit
@app.route('/account', methods=['GET', 'POST'])
def account_page():
    return render_template('account.html')

# delete account (no visual)
@app.route('/account/delete', methods=['GET', 'POST'])
def delete_account():
    return redirect('home_page')

if __name__ == '__main__':
    app.run(debug=True)
