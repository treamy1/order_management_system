'''
CS3250 - Software Development Methods and Tools - Spring 2024
Instructor: Thyago Mota
Students: Travis Reamy, Suar Martinez, Yun Chang, Monica Ball 
Description: Project 01 - Sol Systems Order Manager
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import bcrypt

app = Flask("Authentication Web App")
app.secret_key = 'do not share'
app.config['USER SIGN UP'] = 'User Sign Up'
app.config['USER SIGNIN'] = 'User Sign In'

# db initialization
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

# import models after initializing db
from app import models

# login manager
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

# create the database and add admin user if not exists
with app.app_context():
    db.create_all()

    from app import db
    from app.models import Product

    items = [
    {'code': '101', 'description': '6x8 monocrystalline cell panel, 240W', 'available': True, 'price': 150.00},
    {'code': '202', 'description': '6x10 monocrystalline cell panel, 310W', 'available': True, 'price': 300.00},
    {'code': '303', 'description': '6x12 monocrystalline cell panel, 400W', 'available': True, 'price': 450.00}
    ]

    for item in items:
        # Check if the product already exists to avoid duplicate entries
        existing_product = Product.query.filter_by(code=item['code']).first()
        if not existing_product:
            product = Product(
                code=item['code'],
                description=item['description'],
                availability=item['available'],
                price=item['price']
            )
            db.session.add(product)

    # Commit once outside the loop to save all new products to the database
    db.session.commit()

    # Check if admin user exists
    admin_user = User.query.filter_by(id='tmota').first()
    if not admin_user:
        hashed_password = bcrypt.hashpw('1'.encode('utf-8'), bcrypt.gensalt())
        admin_user = User(
            id='tmota',
            name='Mota',
            passwd=hashed_password,
            # creation_date is automatically set to the current timestamp
        )
        db.session.add(admin_user)
        db.session.commit()
