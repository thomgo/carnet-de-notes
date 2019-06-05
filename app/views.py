from flask import Flask, render_template, redirect
from .models import Thought, db
from .forms import NewThoughtForm

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
@app.route('/index/')
def index():
    thoughts = Thought.query.all()
    return render_template("index.html.j2", thoughts=thoughts)

@app.route('/admin/thought/new', methods=['GET', 'POST'])
def new_thought():
    form = NewThoughtForm()
    if form.validate_on_submit():
        thought = Thought(form.content.data)
        db.session.add(thought)
        db.session.commit()
        return redirect('/index')
    return render_template("admin/new_thought.html.j2", form=form)

@app.route('/admin/thoughts/')
def thoughts():
    thoughts = Thought.query.all()
    return render_template("admin/thoughts.html.j2", thoughts = thoughts)

@app.route('/admin/thought/delete/<int:id>')
def delete_thought(id):
    thought = Thought.query.get(id)
    db.session.delete(thought)
    db.session.commit()
    return redirect('/admin/thoughts/')


if __name__ == "__main__":
    app.run()
