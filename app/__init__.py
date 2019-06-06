import os
from flask import Flask
from flask_login import LoginManager

from .views import app
from . import models

models.db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.cli.command("init_db")
def init_db():
    models.init_db()

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))
