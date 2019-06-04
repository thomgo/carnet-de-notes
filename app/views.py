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

@app.route('/thoughts/new', methods=['GET', 'POST'])
def new_thought():
    form = NewThoughtForm()
    if form.validate_on_submit():
        thought = Thought(form.content.data)
        db.session.add(thought)
        db.session.commit()
        return redirect('/index')
    return render_template("new_thought.html.j2", form=form)

if __name__ == "__main__":
    app.run()
