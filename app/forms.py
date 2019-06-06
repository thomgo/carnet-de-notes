from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from .models import User

class NewThoughtForm(FlaskForm):
    content = StringField('Citation', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')

class LoginForm(FlaskForm):
    pseudo = StringField('Pseudo', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class RegisterForm(FlaskForm):
    last_name = StringField('Nom', validators=[DataRequired()])
    first_name = StringField('Prénom', validators=[DataRequired()])
    pseudo = StringField('Pseudo', validators=[DataRequired()])
    description = TextField('Description personnelle')
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    password_confirm = PasswordField('Confirmez le mot de passe', validators=[DataRequired(), EqualTo('password', "Les deux mot de passes doivent être identiques")])
    submit = SubmitField("S'inscrire")

    def validate_pseudo(self, pseudo):
        user = User.query.filter_by(pseudo=pseudo.data).first()
        if user is not None:
            raise ValidationError('Ce pseudo est déjà pris :(')
