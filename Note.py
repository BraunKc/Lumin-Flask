# Table of notes

from sqlalchemy import ForeignKey
from datetime import datetime

from config import db
from User import User

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.PickleType, ForeignKey(User.id))
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.LargeBinary)
    date = db.Column(db.Date, default=datetime.now)