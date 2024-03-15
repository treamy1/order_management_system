'''
CS3250 - Software Development Methods and Tools - Spring 2024
Instructor: Thyago Mota
Students: Travis Reamy, Suar Martinez, Yun Chang, Monica Ball 
Description: Project 01 - Sol Systems Order Manager
'''

from app import db 
from flask_login import UserMixin
from datetime import datetime, timezone


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    passwd = db.Column(db.LargeBinary)
    creationDate = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'
    admin_id = db.Column(db.String, db.ForeignKey("users.id"), primary_key=True)

class Customer(db.Model, UserMixin):
    __tablename__ = 'customers'
    customer_id = db.Column(db.String, db.ForeignKey("users.id"), primary_key=True)
    address = db.Column(db.String)
    phone_num = db.Column(db.String)
    credit_card_num = db.Column(db.String)
    credit_card_exp = db.Column(db.Date) 
    credit_card_code = db.Column(db.String)

class Recipe(db.Model):
    __tablename__ = 'recipes'
    user_id = db.Column(db.String, db.ForeignKey("users.id"), primary_key=True)
    number = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    type = db.Column(db.String)
    tags = db.Column(db.String)