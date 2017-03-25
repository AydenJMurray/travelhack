from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(Form):
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    #remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField('Log In')

class RegisterForm(Form):
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired(),
                            EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('Repeat Password')

class NewPostForm(Form):
    post = StringField('Post', validators=[DataRequired, Length(1, 64)])
    submit = SubmitField('Post!')
