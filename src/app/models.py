'''
CS3250 - Software Development Methods and Tools - Spring 2024
Instructor: Thyago Mota
Students: Travis Reamy, Suar Martinez, Yun Chang, Monica Ball 
Description: Project 01 - Sol Systems Order Manager
'''

from app import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    about = db.Column(db.String)
    passwd = db.Column(db.LargeBinary)
    recipes = db.relationship("Recipe")

class Recipe(db.Model):
    __tablename__ = 'recipes'
    user_id = db.Column(db.String, db.ForeignKey("users.id"), primary_key=True)
    number = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    type = db.Column(db.String)
    tags = db.Column(db.String)