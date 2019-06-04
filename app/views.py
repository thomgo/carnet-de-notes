from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('config')

@app.route('/index/')
@app.route('/index/<object>')
def index(object=None):
    from .models import Thought
    thoughts = Thought.query.all()
    return render_template("index.html", object=object, thoughts=thoughts)

if __name__ == "__main__":
    app.run()
