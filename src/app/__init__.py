'''
CS3250 - Software Development Methods and Tools - Spring 2024
Instructor: Thyago Mota
Students: Travis Reamy, Suar Martinez, Yun Chang, Monica Ball 
Description: Project 01 - Sol Systems Order Manager
'''

from flask import Flask
import os

app = Flask("Authentication Web App")
app.secret_key = 'do not share'
app.config['USER SIGN UP']= 'User Sign Up"'
app.config['USER SIGNIN']= 'User Sign In"'

# db initialization
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

# import models after initializing db
from app import models

# login manager
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User

# user_loader callback
@login_manager.user_loader
def load_user(id):
    try: 
        return db.session.query(User).filter(User.id==id).one()
    except: 
        return None

# import routes after initializing login_manager
from app import routes

# create the database
with app.app_context(): 
    db.create_all()