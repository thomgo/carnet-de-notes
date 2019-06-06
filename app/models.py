import hashlib

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Create database connection object
db = SQLAlchemy()

class Thought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __init__(self, content):
        self.content = content

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    pseudo = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=True)
    registering_date = db.Column(db.DateTime(), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, last_name, first_name, pseudo, description, registering_date, password):
        self.last_name = last_name
        self.first_name = first_name
        self.pseudo = pseudo
        self.description = description
        self.registering_date = registering_date
        self.password = password

    def set_password(self, password):
         self.password = hashlib.sha256(password).hexdigest()

    def check_password(self, password):
        if hashlib.sha256(password).hexdigest() == self.password:
            return True
        return False


def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("Database initialized !")
