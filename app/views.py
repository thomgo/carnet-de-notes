from flask import Flask
from flask import render_template

app = Flask(__name__)
app.config.from_object('config')

@app.route('/index')
@app.route('/index/<object>')
def index(object=None):
    return render_template("index.html", object=object)

if __name__ == "__main__":
    app.run()
