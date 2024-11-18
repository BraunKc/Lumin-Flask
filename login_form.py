from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', render_kw={'placeholder': 'Email'},
                        validators=[Email('Некорректный email')])

    psw = PasswordField('Password', render_kw={'placeholder': 'Password'},
                        validators=[DataRequired(), Length(min=4, max=100,
                                    message='Длина пароля должна быть от 4 до 100 символов')])

    submit = SubmitField('Войти')
