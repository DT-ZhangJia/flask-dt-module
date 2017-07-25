from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..models import User

class LoginForm(FlaskForm):
    email_input = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    passwd_input = PasswordField('Password', validators=[Required()])
    remember_me_box = BooleanField('Keep me logged in')
    submit_btn = SubmitField('Log In')

class RegisterForm(FlaskForm):
    email_reg_input = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username_reg_input = StringField('Username', validators=[Required(), Length(1, 64), 
                                     Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                     'Usernames must have only letters, numbers, dots or underscores')])
    passwd_reg_input = PasswordField('Password', validators=[Required(),EqualTo('passwd2_reg_input',
                                     message='Passwords must match.')])
    passwd2_reg_input = PasswordField('Confirm password', validators=[Required()])
    submit_reg_btn = SubmitField('Register')

    def validate_email_reg_input(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    
    def validate_username_reg_input(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')