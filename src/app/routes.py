'''
CS3250 - Software Development Methods and Tools - Spring 2024
Instructor: Thyago Mota
Students: Travis Reamy, Suar Martinez, Yun Chang, Monica Ball 
Description: Project 01 - Sol Systems Order Manager
'''

from app import app, db, load_user
from app.models import User, Recipe
from app.forms import SignUpForm, LoginForm, RecipeForm
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
            new_user = User(id=form.id.data, name=form.name.data, about=form.about.data, passwd=hashed_password)
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

@app.route('/users/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        if user and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd):
            login_user(user)
            return redirect(url_for('recipes'))
        else:
            flash('Invalid ID or password', 'error')
    return render_template('login.html', form=form)
    
@app.route('/users/signout', methods=['GET', 'POST'])
def signout():
    logout_user()
    return redirect(url_for('index'))

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