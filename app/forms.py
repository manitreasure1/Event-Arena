from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, EmailField
from wtforms.validators import DataRequired, EqualTo, length, Email

class SignUp(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), length(min=2, max=30)])
    last_name = StringField("Last Name", validators=[DataRequired(), length(min=2, max=30)])
    email = EmailField("Email", validators=[DataRequired(), length(min=10), Email()])
    password = PasswordField("Password", validators=[DataRequired(), length(min=5)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password', message='password must match')])
    submit = SubmitField("Sign Up")


class Login(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), length(min=10), Email()])
    password = PasswordField("Password", validators=[DataRequired(), length(min=5)])
    submit = SubmitField("Login")


class Admin(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

