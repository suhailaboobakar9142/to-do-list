from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,DateField,IntegerField
from wtforms.validators import DataRequired,Length,Email,EqualTo




class RegistrationForm(FlaskForm):
    username=StringField('username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired()])
    confirm_password=PasswordField('confirm password',
                                   validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')


class LoginForm(FlaskForm):
    
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')


class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    description=TextAreaField('description',validators=[DataRequired()])
    duedate=DateField('deu date', validators=[DataRequired()])
    priority=IntegerField('priority',validators=[DataRequired()])
    submit=SubmitField('try')