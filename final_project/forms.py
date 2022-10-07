from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField,PasswordField,SubmitField,FileField,TextAreaField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from final_project.Models import Users

class register_form(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(),Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken.Please choose another')
    def validate_email(self,email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken.Please choose another')


class login_form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class card_form(FlaskForm):
    photo = FileField('Photo',validators=[FileAllowed(['jpg','png'])])

    concept = StringField('Concept',validators=[DataRequired(),Length(min=2, max=50)])

    explanation = TextAreaField('Explanation',validators=[DataRequired()])

    route = SelectField('Select Check Point',validate_choice=True,choices=[])


    submit = SubmitField('Save')

    def validate_username(self,username):
        card = Cards.query.filter_by(name=name.data).first()
        if card:
            raise ValidationError('This card already exists choose another name')
   
class selectPalace_form(FlaskForm):
    name = SelectField('Select the palace to add cards into',validate_choice=True,choices=[])
