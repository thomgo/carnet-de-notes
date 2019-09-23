"""Module that contains the routes with associated methods"""

from datetime import datetime

from flask import Flask, render_template, redirect, flash, request, abort, url_for
from .models import Thought, User, db
from .forms import NewThoughtForm, LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse, urljoin

# Start the app called in run.py and configure it
app = Flask(__name__)
app.config.from_object('config')

def is_safe_url(target):
    """Function to check that the redirection url is safe and from the same server"""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

# Here we define two different routes matching the method
@app.route('/', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    """Function to show login form and check user credentials in database"""
    # if the user is already logged in we send him to the main page
    if current_user.is_authenticated:
        return redirect('/index/')
    # Instance of the form object used to display an HTML form in the view
    form = LoginForm()
    # If the form is correctly filled according to specifications of the forms file
    if form.validate_on_submit():
        # Check in database for user with the given pseudo
        user = User.query.filter_by(pseudo=form.pseudo.data).first()
        # one has been found and the passwords are the same
        # we log him in and redirect to the main page
        if user and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or '/index/')
        # otherwise we show an error message and the login form again
        flash("Pseudo ou mot de passe incorect(s)", "danger")
    return render_template("login.html.j2", form=form)

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
    # Instance of the form object used to display an HTML form in the view
    form = RegisterForm()
    # If the form is correctly filled according to specifications of the forms file
    if form.validate_on_submit():
        try:
            # Instanciate a user object from form data
            user = User(
                last_name = form.last_name.data,
                first_name = form.first_name.data,
                pseudo = form.pseudo.data,
                description = form.description.data
            )
            # Encode the password and store the current date
            user.set_password(form.password.data)
            user.registering_date = datetime.now()
            # Register the user in the Database
            db.session.add(user)
            db.session.commit()
            # Store a success message and go to login page
            flash("Votre compte a été créé", "success")
            return redirect('/login/')
        except Exception as e:
            flash("Une erreur est survenue, nous n'avons pas pu vous enregistrer", "danger")
    return render_template("register.html.j2", form=form)

# ALL THE NEXT ROUTES HAVE THE LOGIN REQUIERED DECORATOR
# BECAUSE THEY ARE RESERVED TO AUTHENTICATED MEMBERS ONLY

@app.route('/index/')
@login_required
def index():
    """Function to show the user thoughts by default"""
    # Retrieve thoughts for a specific user from database
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
    # Instance of the form object used to display an HTML form in the view
    form = NewThoughtForm()
    if form.validate_on_submit():
        # If everything is OK we instanciate a thought objet
        thought = Thought(form.content.data, current_user.id)
        # Register the thought oject in the database and redirect to home page
        db.session.add(thought)
        db.session.commit()
        return redirect('/index')
    return render_template("admin/new_thought.html.j2", form=form)

# This route has a paramater in the url, the id we want to delete
@app.route('/admin/thought/delete/<int:id>')
@login_required
# Do not forget to add an id parameter in the function corresponding to the route parameter
def delete_thought(id):
    """Function to delete a thought in database"""
    # Retrieve the thought object we want to delete by it's id from database
    thought = Thought.query.get(id)
    # if we found a matching thought and it is owned by the logged user we delete it
    if thought and thought.user == current_user:
        db.session.delete(thought)
        db.session.commit()
        flash("Votre note a bien été supprimée", "success")
    return redirect('/admin/thoughts/')

# This route has a paramater in the url, the id of the thought we want to update
@app.route('/admin/thought/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_thought(id):
    """Function to show a form with thought's info and update it in the database"""
    # Retrieve the thought object we want to update by it's id from database
    thought = Thought.query.get(id)
    # If do not find the thougth or it is not owned by the user we redirect with error message
    if not thought or thought.user != current_user:
        flash("Il semble qu'il y ait eu un problème", "danger")
        return redirect("/admin/thoughts/")
    # Instance of the form object used to display a prefilled form in the view
    form = NewThoughtForm(obj=thought)
    if form.validate_on_submit():
        # update the content in the object NOT the database
        thought.content = form.content.data
        # update the database
        db.session.commit()
        return redirect('/admin/thoughts/')
    return render_template('admin/update_thought.html.j2', thought=thought, form=form)
