from flask import Flask, render_template, redirect
from .models import Thought, User, db
from .forms import NewThoughtForm, LoginForm
from flask_login import login_user, logout_user

app = Flask(__name__)
app.config.from_object('config')

@app.route('/', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(pseudo=form.pseudo.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/index")
    return render_template("login.html.j2", thoughts=thoughts, form=form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/login/')

@app.route('/index/')
def index():
    thoughts = Thought.query.all()
    return render_template("index.html.j2", thoughts=thoughts)


@app.route('/admin/thoughts/')
def thoughts():
    thoughts = Thought.query.all()
    return render_template("admin/thoughts.html.j2", thoughts = thoughts)

@app.route('/admin/thought/new', methods=['GET', 'POST'])
def new_thought():
    form = NewThoughtForm()
    if form.validate_on_submit():
        thought = Thought(form.content.data)
        db.session.add(thought)
        db.session.commit()
        return redirect('/index')
    return render_template("admin/new_thought.html.j2", form=form)

@app.route('/admin/thought/delete/<int:id>')
def delete_thought(id):
    thought = Thought.query.get(id)
    db.session.delete(thought)
    db.session.commit()
    return redirect('/admin/thoughts/')

@app.route('/admin/thought/update/<int:id>', methods=['GET', 'POST'])
def update_thought(id):
    thought = Thought.query.get(id)
    form = NewThoughtForm(obj=thought)
    if form.validate_on_submit():
        thought.content = form.content.data
        db.session.commit()
        return redirect('/admin/thoughts/')
    return render_template('admin/update_thought.html.j2', thought=thought, form=form)


if __name__ == "__main__":
    app.run()
