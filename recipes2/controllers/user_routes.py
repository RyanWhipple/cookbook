import re
from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from recipes2 import db, bcrypt
from recipes2.models.user import User, Follower
from recipes2.models.recipe import Recipe
from recipes2.models.result import Result
from recipes2.forms.user_forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from recipes2.utils.utils import save_picture, send_reset_email
from sqlalchemy import or_
from flask_paginate import Pagination




EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
users = Blueprint('users', __name__)


@users.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name      = form.first_name.data,
                    last_name       = form.last_name.data,
                    username        = form.username.data,
                    email           = form.email.data,
                    password        = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        login_user(user, remember=False)
        return redirect(url_for('main.home'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET'])
@login_required
def account():

    page = request.args.get('page', 1, type=int)
    per_page = 6
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    followees = Follower.query.filter_by(follower_id = current_user.id).paginate(page=page, per_page=per_page)

    followers = Follower.query.filter_by(followee_id = current_user.id).paginate(page=page, per_page=per_page)

    return render_template('account.html', title='Account', image_file=image_file, followees=followees, followers=followers)



@users.route('/account_edit', methods=['GET', 'POST'])
@login_required
def account_edit():
    form = UpdateAccountForm()

    if request.method == 'GET':
        form.first_name.data    = current_user.first_name
        form.last_name.data     = current_user.last_name
        form.username.data      = current_user.username
        form.email.data         = current_user.email
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
        return render_template('account_edit.html', title='Account', image_file=image_file, form=form)
    
    elif request.method == "POST":
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data, "profile_pics/")
                current_user.image_file = picture_file
            current_user.first_name     = form.first_name.data
            current_user.last_name      = form.last_name.data
            current_user.username       = form.username.data
            current_user.email          = form.email.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('users.account'))
    

# My Recipes
@users.route('/user/<string:username>/recipes')
def user_recipes(username):
    page = request.args.get('page', 1, type=int)
    per_page = 6
    # offset = (page-1) * per_page THIS ISN'T REQUIRED WHEN WORKING WITH A PAGINATED QUERY OBJECT INSTEAD OF A LIST
    user = User.query.filter_by(username=username).first_or_404()
    recipes = Recipe.query\
                .filter(or_(Recipe.public==1,(current_user.is_authenticated and Recipe.user == current_user)))\
                .filter_by(user=user)\
                .order_by(Recipe.created_at.desc())\
                .paginate(page=page, per_page=per_page)
    total = Recipe.query.filter(or_(Recipe.public==1,(current_user.is_authenticated and Recipe.user == current_user))).filter_by(user=user).count()
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    return render_template('user_recipes.html', title='Home', recipes=recipes, user=user, pagination=pagination)


# My Results
@users.route('/user/<string:username>/results')
def user_results(username):
    page = request.args.get('page', 1, type=int)
    per_page = 6
    # offset = (page-1) * per_page THIS ISN'T REQUIRED WHEN WORKING WITH A PAGINATED QUERY OBJECT INSTEAD OF A LIST
    user = User.query.filter_by(username=username).first_or_404()
    results = Result.query\
                .filter(or_(Result.recipe_id.in_([recipe.id for recipe in Recipe.query.filter_by(public=1)]),(current_user.is_authenticated and Result.user_id == current_user.id)))\
                .filter_by(user=user)\
                .order_by(Result.created_at.desc())\
                .paginate(page=page, per_page=6)
    total = Result.query\
                .filter(or_(Result.recipe_id.in_([recipe.id for recipe in Recipe.query.filter_by(public=1)]),(current_user.is_authenticated and Result.user_id == current_user.id)))\
                .filter_by(user=user).count()
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    return render_template('user_results.html', title='Home', results=results, user=user, pagination = pagination)


@users.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user != current_user:
        abort(403)
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted!', 'success')
    return redirect(url_for('main.home'))


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been changed!  You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@users.route('/ajax/user/username', methods=["POST"])
def validate_username_ajax():
    invalid = '';
    if len(request.form['username']) < 3:
        invalid = 'short'
        return render_template('partials/username.html', invalid=invalid)
    user = User.query.filter_by(username=request.form['username']).first()
    if user:
        invalid = 'taken'
        return render_template('partials/username.html', invalid=invalid)
    return render_template('partials/username.html', invalid=invalid)

@users.route('/ajax/user/email', methods=["POST"])
def validate_email_ajax():
    invalid = '';
    if not EMAIL_REGEX.match(request.form['email']):
        invalid = 'not_email'
        return render_template('partials/email.html', invalid=invalid)
    user = User.query.filter_by(email=request.form['email']).first()
    if user:
        invalid = 'taken'
        return render_template('partials/email.html', invalid=invalid)
    return render_template('partials/email.html', invalid=invalid)

@users.route('/ajax/user/password', methods=["POST"])
def validate_password_ajax():
    invalid = len(request.form['password']) < 8;
    return render_template('partials/password.html', invalid=invalid)

@users.route('/ajax/user/confirm_password', methods=["POST"])
def validate_confirm_password_ajax():
    invalid = not request.form['password'] == request.form['confirm_password'] ;
    return render_template('partials/confirm_password.html', invalid=invalid)