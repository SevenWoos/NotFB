from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Enum

from extensions import db  # if you're importing db from app.py

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(Enum('user', 'admin', name='user_roles'), nullable=False, default='user')
    bio = db.Column(db.String(500), nullable=True)
    profile_picture = db.Column(db.String(120), nullable=True)
    
