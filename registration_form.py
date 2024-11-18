from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegisterForm(FlaskForm):
    email = StringField('Email', render_kw={'placeholder': 'Email'},
                        validators=[Email('Некорректный email')])

    username = StringField('Name', render_kw={'placeholder': 'Name'},
                           validators=[DataRequired(), Length(min=2, max=50,
                                        message='Длина имени должна быть от 2 до 50 символов')])

    psw = PasswordField('Password', render_kw={'placeholder': 'Password'},
                        validators=[DataRequired(), Length(min=4, max=100,
                                    message='Длина пароля должна быть от 4 до 100 символов')])

    confirm_psw = PasswordField('Confirm password', render_kw={'placeholder': 'Confirm password'},
                                validators=[EqualTo('psw')])

    submit = SubmitField('Зарегистрироваться')
