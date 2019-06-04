from flask_sqlalchemy import SQLAlchemy

# Create database connection object
db = SQLAlchemy()

class Thought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __init__(self, content):
        self.content = content


def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(Thought("Une pensée parmis d'autres"))
    db.session.add(Thought("l'homme est un loup pour l'homme"))
    db.session.add(Thought("Une idée simple est une bonne idée"))
    db.session.commit()
    print("Database initialized !")
