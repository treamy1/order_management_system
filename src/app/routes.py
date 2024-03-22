'''
CS3250 - Software Development Methods and Tools - Spring 2024
Instructor: Thyago Mota
Students: Travis Reamy, Suar Martinez, Yun Chang, Monica Ball 
Description: Project 01 - Sol Systems Order Manager
'''

from app import app, db, load_user
from app.models import User, Recipe, Order, Product, Customer, Administrator, Item
from app.forms import SignUpForm, LoginForm, RecipeForm, OrderForm, ProductForm
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
    orders = Order.query.all()
    products = Product.query.all()  # Retrieve all products from the database

    if current_user.id in admin_id:  # Check if current user is an admin
        return render_template('admin.html', admin=current_user, orders=orders, products=products)
    else:
        return redirect(url_for('index'))
    
@app.route('/admin/order/<int:order_number>/update', methods=['POST'])
@login_required
def update_order_status(order_number):
    order = Order.query.filter_by(number=order_number).first()
    if order:
        order.status = request.form['status']
        db.session.commit()
        flash('Order status updated successfully!', 'success')
    else:
        flash('Order not found.', 'error')
    
    return redirect(url_for('admin'))

    
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


@app.route('/orders')
@login_required
def orders():
    # Assuming current_user.orders automatically fetches the orders for the logged-in user
    return render_template('orders.html', orders=current_user.orders)


@app.route('/orders/create', methods=['GET', 'POST'])
@login_required
def orders_create():
    form = OrderForm()  # Initialize the form here
    products = Product.query.all()

    # Check if the current user already has a customer record
    existing_customer = Customer.query.filter_by(customer_id=current_user.id).first()

    if request.method == 'POST':
        # Only create a new customer if one doesn't exist
        if not existing_customer:
            customer = Customer(
                customer_id=current_user.id,
                address=form.address.data,
                phone=form.phone.data,
                credit_card_number=form.credit_card_number.data,
                credit_card_exp_date=form.credit_card_exp_date.data,
                credit_card_code=form.credit_card_code.data
            )
            db.session.add(customer)

        # Create a new order instance
        new_order = Order(
            creation_date=datetime.utcnow(),
            status='new',
            user_id=current_user.id
        )
        db.session.add(new_order)
        db.session.flush()  # To get the new_order.id for foreign key reference

        # Process each product's quantity from the form
        seq_number = 1
        total_price = 0
        for product in products:
            quantity = int(request.form.get(f'quantity_{product.code}', 0))
            total_price += quantity * product.price

            for _ in range(quantity):  # Loop based on the quantity to create individual item instances
                item = Item(
                    sequential_number=seq_number,
                    order_number=new_order.number,
                    product_code=product.code,
                    quantity=1,  # Since you are creating an instance per unit, quantity is always 1
                    price=product.price
                )
                db.session.add(item)
                seq_number += 1

        db.session.commit()
        print('Order created successfully!', 'success')
        return redirect(url_for('orders'))

    # If GET request or not yet posted, render the form
    return render_template('orders_create.html', form=form, products=products, existing_customer=existing_customer)





@app.route('/orders/<int:number>/delete', methods=['GET', 'POST'])
@login_required
def orders_delete(number):
    # Assuming 'number' is a unique identifier for Order
    order_to_delete = Order.query.filter_by(number=number, user_id=current_user.id).first()
    if order_to_delete:
        db.session.delete(order_to_delete)
        db.session.commit()
        print('Order deleted successfully!', 'success')
    else:
        print('Order not found or you do not have permission to delete it.', 'error')
    
    return redirect(url_for('orders'))


@app.route('/admin/product/add', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            code=form.code.data,
            description=form.description.data,
            availability=form.availability.data,
            price=form.price.data
        )
        db.session.add(product)
        try:
            db.session.commit()
            flash('Product added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error adding product: ' + str(e), 'error')
        return redirect(url_for('admin'))
    return render_template('product_form.html', form=form, title="Add Product")

@app.route('/admin/product/edit/<code>', methods=['GET', 'POST'])
@login_required
def edit_product(code):
    product = Product.query.get_or_404(code)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.code = form.code.data
        product.description = form.description.data
        product.availability = form.availability.data
        product.price = form.price.data
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin'))
    return render_template('product_form.html', form=form, title="Edit Product")

@app.route('/admin/product/delete/<code>', methods=['POST'])
@login_required
def delete_product(code):
    product = Product.query.get_or_404(code)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin'))





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


