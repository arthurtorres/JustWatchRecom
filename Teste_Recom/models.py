# models.py

from flask_login import UserMixin
from .extensions import db 

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    country = db.Column(db.String(1000))

class Series(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True,) # primary keys are required by SQLAlchemy
    id_user =db.Column(db.Integer)
    Serie = db.Column(db.String(1000))
    Recom = db.Column(db.String(1000))

