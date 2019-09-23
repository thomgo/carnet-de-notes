"""Module to hold the different forms for the application"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Regexp

from .models import User

# Note that each form corresponds to an entities from the model
# Form fields are defiened by class attributs holding object of the correspnding type field

class NewThoughtForm(FlaskForm):
    """ Class to generate a form to add a thought to the database"""
    content = StringField('Citation', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')

class LoginForm(FlaskForm):
    """ Class to generate a form for the login"""
    pseudo = StringField('Pseudo', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class RegisterForm(FlaskForm):
    """ Class to generate a form for the user to register on the site"""
    last_name = StringField('Nom', validators=[DataRequired()])
    first_name = StringField('Prénom', validators=[DataRequired()])
    pseudo = StringField('Pseudo', validators=[DataRequired()])
    description = TextField('Description personnelle')
    password = PasswordField('Mot de passe', validators=[
        DataRequired(),
        Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{6,}$", message="Attention le mot de passe doit contenir 6 caractères, une minuscule, une majuscule et un chiffre")
    ])
    password_confirm = PasswordField('Confirmez le mot de passe', validators=[
        DataRequired(),
        EqualTo('password', "Les deux mot de passes doivent être identiques")
    ])
    submit = SubmitField("S'inscrire")

    # NOTE: this a special validation system from wtfform
    # each method of a form starting with validate_ + the field name is called when submitting the form
    def validate_pseudo(self, pseudo):
        """Function that checks that the pseudo is not already used in database"""
        user = User.query.filter_by(pseudo=pseudo.data).first()
        if user is not None:
            raise ValidationError('Ce pseudo est déjà pris :(')
