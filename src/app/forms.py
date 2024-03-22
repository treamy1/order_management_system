'''
CS3250 - Software Development Methods and Tools - Spring 2024
Instructor: Thyago Mota
Students: Travis Reamy, Suar Martinez, Yun Chang, Monica Ball 
Description: Project 01 - Sol Systems Order Manager
'''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, validators
from wtforms.validators import DataRequired

class SignUpForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    # about = StringField('About', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    passwd_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class LoginForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

# working on for order form with routes currently.
class OrderForm(FlaskForm):
    number = StringField('Order#', validators=[DataRequired()])
    creationDate = StringField('Creation Date', validators=[DataRequired()])
    status = SelectField('Status', choices=['new', 'in progress', 'completed'], validators=[DataRequired()])
    items = StringField('Items', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class RecipeForm(FlaskForm):
    number = StringField('Recipe#', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    type = SelectField('Type', choices=['breakfast', 'appetizer', 'side dish', 'main course', 'dessert'], validators=[DataRequired()])
    tags = StringField('Tags')
    submit = SubmitField('Submit')