from flask import Flask, render_template
from .models import Thought

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
@app.route('/index/')
def index():
    thoughts = Thought.query.all()
    return render_template("index.html.j2", thoughts=thoughts)

if __name__ == "__main__":
    app.run()
