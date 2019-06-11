"""Module the contains the routes with associated methods"""

from datetime import datetime

from flask import Flask, render_template, redirect, flash, request, abort, url_for
from .models import Thought, User, db
from .forms import NewThoughtForm, LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse, urljoin

app = Flask(__name__)
app.config.from_object('config')

def is_safe_url(target):
    """Function to check that the redirection url is safe and from the same server"""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@app.route('/', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    """Function to show login form and check user credentials in database"""
    if current_user.is_authenticated:
        return redirect('/index/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(pseudo=form.pseudo.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or '/index/')
        flash("Pseudo ou mot de passe incorect(s)", "danger")
    return render_template("login.html.j2", thoughts=thoughts, form=form)

@app.route('/logout/')
@login_required
def logout():
    """Function to log the user out with flask_login"""
    logout_user()
    flash("Vous avez bien été déconnecté", "success")
    return redirect('/login/')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Function to show a registration form and save a new user in database"""
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            last_name = form.last_name.data,
            first_name = form.first_name.data,
            pseudo = form.pseudo.data,
            description = form.description.data
        )
        user.set_password(form.password.data)
        user.registering_date = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("Votre compte a été créé", "success")
        return redirect('/login/')
    return render_template("register.html.j2", form=form)

@app.route('/index/')
@login_required
def index():
    """Function to show the user thoughts by default"""
    thoughts = Thought.query.filter_by(user=current_user).all()
    return render_template("index.html.j2", thoughts=thoughts)


@app.route('/admin/thoughts/')
@login_required
def thoughts():
    """Function to show the thoughts in the admin panel"""
    thoughts = Thought.query.filter_by(user=current_user).all()
    return render_template("admin/thoughts.html.j2", thoughts = thoughts)

@app.route('/admin/thought/new', methods=['GET', 'POST'])
@login_required
def new_thought():
    """Function to show a form and add a thought in database"""
    form = NewThoughtForm()
    if form.validate_on_submit():
        thought = Thought(form.content.data, current_user.id)
        db.session.add(thought)
        db.session.commit()
        return redirect('/index')
    return render_template("admin/new_thought.html.j2", form=form)

@app.route('/admin/thought/delete/<int:id>')
@login_required
def delete_thought(id):
    """Function to delete a thought in database"""
    thought = Thought.query.get(id)
    if thought and thought.user == current_user:
        db.session.delete(thought)
        db.session.commit()
        flash("Votre note a bien été supprimée", "success")
    return redirect('/admin/thoughts/')

@app.route('/admin/thought/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_thought(id):
    """Function to show a form with thought's info and update it in the database"""
    thought = Thought.query.get(id)
    if not thought or thought.user != current_user:
        flash("Il semble qu'il y ait eu un problème", "danger")
        return redirect("/admin/thoughts/")
    form = NewThoughtForm(obj=thought)
    if form.validate_on_submit():
        thought.content = form.content.data
        db.session.commit()
        return redirect('/admin/thoughts/')
    return render_template('admin/update_thought.html.j2', thought=thought, form=form)


if __name__ == "__main__":
    app.run()
