'''
CS3250 - Software Development Methods and Tools - Spring 2024
Instructor: Thyago Mota
Students: Travis Reamy, Suar Martinez, Yun Chang, Monica Ball 
Description: Project 01 - Sol Systems Order Manager
'''

from app import app, db, load_user
from app.models import User, Recipe, Order, Product, Customer, Administrator
from app.forms import SignUpForm, LoginForm, RecipeForm, OrderForm
from datetime import datetime, timezone
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt



            
@app.route('/')
@app.route('/index')
@app.route('/index.html')

def index(): 
    return render_template('index.html')

@app.route('/users/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if form.passwd.data == form.passwd_confirm.data:
            hashed_password = bcrypt.hashpw(form.passwd.data.encode('utf-8'), bcrypt.gensalt())
            new_user = User(id=form.id.data, name=form.name.data, passwd=hashed_password)
            db.session.add(new_user)
            try:
                db.session.commit()
                return redirect(url_for('index'))
            except:
                db.session.rollback()
                flash('ID already exists or error in database operation', 'error')
        else:
            flash('Passwords do not match', 'error')
    return render_template('signup.html', form=form)

# create admin page
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():

    adminUser = User.query.filter_by(id='tmota').first()
    admin_id = adminUser.id

    if current_user.id in admin_id:  # Check if current user is an admin
        return render_template('admin.html', admin=current_user)
    else:
        return redirect(url_for('index'))
    
@app.route('/users/login', methods=['GET', 'POST'])
def login():

    adminUser = User.query.filter_by(id='tmota').first()
    admin_id = adminUser.id

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        if user and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd):
            login_user(user)
            if user.id in admin_id:  # Check if user ID is in admin_id list

                # print(adminUser.creation_date)
                
                return redirect(url_for('admin'))  # Redirect admin to admin page
            else:
                return redirect(url_for('orders'))  # Redirect regular user to orders page
        else:
            return redirect(url_for('login_failed'))  # Incorrect credentials
    return render_template('login.html', form=form)

@app.route('/users/signout', methods=['GET', 'POST'])
def signout():
    logout_user()
    return redirect(url_for('index'))

# defined list of products
'''
items=[
    {'code': 101,'description': '6x8 monocrystalline cell panel, 240W','available': True,'price': 150.00},
    {'code': 202,'description': '6x10 monocrystalline cell panel, 310W','available': True,'price': 300.00},
    {'code': 303,'description': '6x12 monocrystalline cell panel, 400W','available': True, 'price': 450.00}
]
'''

@app.route('/orders')
@login_required
def orders():
    return render_template('orders.html', user=current_user)

@app.route('/orders/create', methods=['GET','POST'])
def orders_create():
    form = OrderForm()
    if form.validate_on_submit():
        new_recipe = Recipe(user_id=current_user.id, number=form.number.data, creationDate=form.creationDate.data, status=form.status.data, items=form.items.data)
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('orders'))
    else:
        return render_template('orders_create.html', form=form) 

@app.route('/orders/<number>/delete', methods=['GET', 'POST'])
@login_required
def orders_delete(number):
    order_to_delete = Recipe.query.filter_by(number=number, user_id=current_user.id).first()
    if order_to_delete:
        db.session.delete(order_to_delete)
        db.session.commit()
    return redirect(url_for('orders'))
'''
# design the orders form
@app.route('/products')
@login_required
def products():
    return render_template('products.html', user=current_user)

@app.route('/products/create', methods=['GET','POST'])
@login_required
def orders_create():
    form = OrdersForm()
    if form.validate_on_submit():
        new_order = Order(user_id=current_user.id, number=form.number.data, status=form.status.data, creationDate=form.creationDate.data, items=form.items.data)
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for('products'))
    else:
        return render_template('orders_create.html', form=form)

@app.route('/products/<number>/delete', methods=['GET', 'POST'])
@login_required
def products_delete(id):
    product_to_delete = Product.query.filter_by(id=id, user_id=current_user.id).first()
    if product_to_delete:
        db.session.delete(product_to_delete)
        db.session.commit()
    return redirect(url_for('products'))

'''

# function to handle login/signup failed
@app.route('/users/login_failed')
def login_failed():
    return render_template('login_failed.html')


@app.route('/recipes')
@login_required
def recipes(): 
    return render_template("recipes.html", user=current_user)

@app.route('/recipes/create', methods=['GET','POST'])
@login_required
def recipes_create():
    form = RecipeForm()
    if form.validate_on_submit():
        new_recipe = Recipe(user_id=current_user.id, number=form.number.data, title=form.title.data, type=form.type.data, tags=form.tags.data)
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('recipes'))
    else:
        return render_template('recipes_create.html', form=form)

@app.route('/recipes/<number>/delete', methods=['GET', 'POST'])
@login_required
def recipes_delete(number):
    recipe_to_delete = Recipe.query.filter_by(number=number, user_id=current_user.id).first()
    if recipe_to_delete:
        db.session.delete(recipe_to_delete)
        db.session.commit()
    return redirect(url_for('recipes'))