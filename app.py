from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user

from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
import hashlib
import base64

from config import *
from User import User
from Note import Note

# WTFORMS
from login_form import *
from registration_form import *


@login_manager.user_loader
def load_user(user_id):
    """
    Load user by ID for Flask-Login.

    :param user_id: User ID
    :return: User object
    """
    return User.query.get(int(user_id))


@app.route('/')
def home_page():
    """
    Home page route.

    :return: Rendered home page template
    """
    return render_template('home.html', title='Lumin')


'''
User database
Routes for user registration, login, and logout
'''


@app.route('/registration', methods=['GET', 'POST'])
def registration_page():
    """
    User registration page route.

    :return: Redirect to notes page if user is authenticated, or render registration form
    """
    if current_user.is_authenticated:
        return redirect(url_for('notes_page'))

    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit:
        email = form.email.data
        username = form.username.data
        psw = generate_password_hash(form.psw.data)

        user = User(email=email, username=username, password=psw)

        try:
            db.session.add(user)
            db.session.commit()

            login_user(user)

            return redirect(url_for('notes_page'))
        except:
            return 'Save error'
    return render_template('authentication.html', title='Lumin', action='register',
                           RegisterForm=RegisterForm(), LoginForm=LoginForm())

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """
    User login page route.

    :return: Redirect to notes page if user is authenticated, or render login form
    """
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
        elif not user:
            return 'Invalid email', 401
        else:
            return 'Invalid password'
    return render_template('authentication.html', title='Lumin', action='login',
                           RegisterForm=RegisterForm(), LoginForm=LoginForm())

@app.route('/logout')
def logout():
    """
    User logout route.

    :return: Redirect to home page
    """
    logout_user()
    return redirect(url_for('home_page'))


'''
Note database
Routes for adding, updating, and deleting notes
'''


def encrypt_data(data: str) -> bytes:
    """
    Encrypt note content using user's password.

    :param data: Note content
    :return: Encrypted note content
    """
    sha256_hash = hashlib.sha256(current_user.password.encode('utf-8')).digest()
    key = base64.urlsafe_b64encode(sha256_hash)
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
    return encrypted_data


# Return decrypted content of note
def decrypt_data(data) -> dict:
    """
    Decrypt note content using user's password.

    :param data: Note object
    :return: Decrypted note content
    """
    sha256_hash = hashlib.sha256(current_user.password.encode('utf-8')).digest()
    key = base64.urlsafe_b64encode(sha256_hash)

    content = Fernet(key).decrypt(data.content).decode('utf-8')

    note = {
        'id': data.id,
        'user_id': data.user_id,
        'title': data.title,
        'content': content,
        'date': data.date
    }
    return note


# Page with all notes
@app.route('/notes')
def notes_page():
    """
    Notes page route.

    :return: Rendered notes page template
    """
    own_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.date).all()

    return render_template('notes.html', title='Lumin | Notes', own_notes=own_notes)


# Page for creating a note (no visual)
@app.route('/notes/create', methods=['POST'])
def create_note():
    """
    Create note route.

    :return: JSON response or error message
    """
    if request.method == 'POST':
        data = request.get_json()
        title = data['title']
        content = encrypt_data(data['content'])

        note = Note(user_id=current_user.id, title=title, content=content)

        try:
            db.session.add(note)
            db.session.commit()
        except:
            return 'Add to database error'


# Note page, user can edit note
@app.route('/notes/<int:note_id>', methods=['GET', 'POST'])
def note_page(note_id: int):
    """
    Note page route.

    :param note_id: Note ID
    :return: Rendered note page template
    """
    note = Note.query.get_or_404(note_id)
    own_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.date).all()

    if request.method == 'POST':
        data = request.get_json()
        note.title = data['title']
        note.content = encrypt_data(data['content'])

        try:
            db.session.commit()
        except:
            print('Edit database error')
    return render_template('note.html', title=note.title, own_notes=own_notes, note=decrypt_data(note))


# Page for deleting a note (no visual)
@app.route('/notes/<int:note_id>/delete', methods=['GET', 'POST'])
def delete_note(note_id: int):
    """
    Delete note route.

    :param note_id: Note ID
    :return: Redirect to notes page or error message
    """
    note = Note.query.get_or_404(note_id)

    try:
        db.session.delete(note)
        db.session.commit()
    except:
        return 'Delete note error'
    return redirect(url_for('notes_page'))


'''
User database
Routes for updating and deleting user account
'''


# Account page (information about user), can edit password
@app.route('/account', methods=['GET', 'POST'])
def account_page():
    """
    Account page route.

    :return: Rendered account page template
    """
    if request.method == 'POST':
        password = request.get_json()['password']

        try:
            current_user.password = generate_password_hash(password)
            db.session.commit()
        except:
            return 'Update password error'
    return render_template('account.html', title=f'Account | {current_user.username}', user=current_user)


# Page for deleting account (no visual)
@app.route('/account/delete', methods=['GET', 'POST'])
def delete_account():
    """
    Delete account route.

    :return: Redirect to home page or error message
    """
    try:
        notes = Note.query.filter_by(user_id=current_user.id).all()

        for note in notes:
            db.session.delete(note)

        try:
            db.session.delete(current_user)
            db.session.commit()
            return redirect(url_for('home_page'))
        except:
            return 'User delete error'
    except:
        return 'Notes delete error'


if __name__ == '__main__':
    app.run(debug=True)