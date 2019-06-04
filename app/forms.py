from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NewThoughtForm(FlaskForm):
    content = StringField('Citation', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')
