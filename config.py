from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'e9cd7aea3834817c0113dc7ef57c9d25'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
