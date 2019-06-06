import os
from flask import Flask
from flask_login import LoginManager

from .views import app
from . import models

models.db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@app.cli.command("init_db")
def init_db():
    models.init_db()
