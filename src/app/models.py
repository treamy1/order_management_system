'''
CS3250 - Software Development Methods and Tools - Spring 2024
Instructor: Thyago Mota
Students: Travis Reamy, Suar Martinez, Yun Chang, Monica Ball 
Description: Project 01 - Sol Systems Order Manager
'''

from app import db 
from flask_login import UserMixin
from datetime import datetime, timezone


from app import db
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    passwd = db.Column(db.String)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.String, db.ForeignKey('users.id'), primary_key=True)

    address = db.Column(db.String)
    phone = db.Column(db.String)
    credit_card_number = db.Column(db.String)
    credit_card_exp_date = db.Column(db.String)  # Assuming string format for expiration date
    credit_card_code = db.Column(db.String)

    # Define relationship with User
    user = db.relationship('User', backref='customer', lazy=True)

class Administrator(db.Model):
    __tablename__ = 'administrators'
    admin_id = db.Column(db.String, db.ForeignKey('users.id'), primary_key=True)

    # Define relationship with User
    user = db.relationship('User', backref='administrator', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    code = db.Column(db.String, primary_key=True)
    description = db.Column(db.String)
    availability = db.Column(db.Boolean) # true/false
    price = db.Column(db.Float)

class Order(db.Model):
    __tablename__ = 'orders'
    number = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String)

    user_id = db.Column(db.String, db.ForeignKey('users.id'))

    # Define relationship with User
    user = db.relationship('User', backref='orders', lazy=True)

    # Define relationship with Item
    items = db.relationship('Item', backref='order', lazy=True)


class Item(db.Model):
    __tablename__ = 'items'
    item_id = db.Column(db.Integer, primary_key=True) # create primary key for items
    sequential_number = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

    # relationship with product
    product_code = db.Column(db.String, db.ForeignKey('products.code'))
    # relationship with order
    order_number = db.Column(db.Integer, db.ForeignKey('orders.number'))

class Recipe(db.Model):
    __tablename__ = 'recipes'
    # relationship with user
    user_id = db.Column(db.String, db.ForeignKey("users.id"), primary_key=True)
    number = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    type = db.Column(db.String)
    tags = db.Column(db.String)