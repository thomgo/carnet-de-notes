from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class NewThoughtForm(FlaskForm):
    content = StringField('Citation', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')

class LoginForm(FlaskForm):
    pseudo = StringField('Pseudo', validators=[DataRequired()])
    password = PasswordField('Mot de Passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')
