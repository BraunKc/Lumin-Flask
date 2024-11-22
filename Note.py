# Table of notes

from datetime import datetime

from config import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.LargeBinary)
    date = db.Column(db.Date, default=datetime.now)
