"""Module to hold the entities class stored in the database with sqlalchemy"""

import hashlib
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Create database connection object
db = SQLAlchemy()

class Thought(db.Model):
    """Represent a Thought entity, basically a sentence from a user"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    #Relation with the user who has written the thought
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

class User(UserMixin, db.Model):
    """Represent a User entity with credentials for authentication from UserMixin"""
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    pseudo = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=True)
    registering_date = db.Column(db.DateTime(), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    #Store all the thoughts published by a user
    thoughts = db.relationship('Thought', backref='user', lazy=True)

    def __init__(self, last_name, first_name, pseudo, description, registering_date=None, password=None):
        self.last_name = last_name
        self.first_name = first_name
        self.pseudo = pseudo
        self.description = description
        self.registering_date = registering_date
        self.password = password

    def set_password(self, password):
        """Function to hash the password before setting it in the attribut"""
        self.password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    def check_password(self, password):
        """Function to check that the user password match another password"""
        if hashlib.sha256(password.encode('utf-8')).hexdigest() == self.password:
            return True
        return False

def init_db():
    """Function to init the database tables with a sample user"""
    db.drop_all()
    db.create_all()
    user = User("test", "test", "test", None, datetime.now(), None)
    user.set_password("Test1234")
    db.session.add(user)
    db.session.commit()
    print("Database initialized !")
