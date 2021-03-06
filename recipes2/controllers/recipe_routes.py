from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from recipes2 import db
from recipes2.models.recipe import Recipe
from recipes2.models.result import Result
from recipes2.forms.recipe_forms import RecipeForm
from recipes2.forms.result_forms import ResultForm
from recipes2.utils.utils import save_picture
from flask_paginate import Pagination

recipes = Blueprint('recipes', __name__)

@recipes.route('/recipe/new', methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()

    # Display Blank Form
    if request.method == "GET":
        return render_template('recipe_create_update.html', title='New Recipe', form=form, legend='New Recipe')
    
    # Save Filled-in Form
    elif request.method == "POST":
        if form.validate_on_submit():
            
            if form.picture.data:
                picture_file = save_picture(form.picture.data, "recipe_pics/")
            else:
                picture_file = "default_food.png"
            
            recipe = Recipe(name                = form.name.data,
                            description         = form.description.data,
                            prep_time           = form.prep_time.data,
                            cook_time           = form.cook_time.data,
                            image_file          = picture_file,
                            public              = 1 if form.public.data else 0,
                            ingredients         = form.ingredients.data,
                            instructions        = form.instructions.data,
                            notes               = form.notes.data,
                            user                = current_user)
            db.session.add(recipe)
            db.session.commit()
            flash('Your recipe has been created!','success')
            return redirect(url_for('main.home'))
        else:
            print("new_recipe form.validate_on_submit() failed")
            return render_template('recipe_create_update.html', title='New Recipe', form=form, legend='New Recipe')

    


@recipes.route('/recipe/<int:recipe_id>/update', methods=['GET', 'POST'])
@login_required
def update_recipe(recipe_id):
    form = RecipeForm()
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user != current_user:
        abort(403)

    # Display form filled-in with Recipe's current data
    if request.method == 'GET':
            form.name.data          = recipe.name
            form.description.data   = recipe.description
            form.prep_time.data     = recipe.prep_time
            form.cook_time.data     = recipe.cook_time
            form.public.data        = recipe.public > 0
            form.ingredients.data   = recipe.ingredients
            form.instructions.data  = recipe.instructions
            form.notes.data         = recipe.notes
            return render_template('recipe_create_update.html', title='Update Recipe', form=form, legend='Update Recipe', recipe=recipe)

    # Save updated form
    elif request.method == "POST":
        if form.validate_on_submit():
            recipe.name         = form.name.data
            recipe.description  = form.description.data
            recipe.prep_time    = form.prep_time.data
            recipe.cook_time    = form.cook_time.data
            
            if form.picture.data:
                picture_file = save_picture(form.picture.data, "recipe_pics/")
                recipe.image_file = picture_file
            recipe.public       = 1 if form.public.data else 0
            recipe.ingredients  = form.ingredients.data
            recipe.instructions = form.instructions.data
            recipe.notes        = form.notes.data
            db.session.commit()
            flash('Your recipe has been updated!', 'success')
            return redirect(url_for('recipes.recipe', recipe_id=recipe.id))
        else:
            print("update_recipe form.validate_on_submit() failed")
            return render_template('recipe_create_update.html', title=recipe.name, form=form, legend=recipe.name)
    


@recipes.route('/recipe/<int:recipe_id>/', methods=['GET', 'POST'])
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    result_form = ResultForm()
    if recipe.public == 0 and recipe.user != current_user:
        abort(403)
    page = request.args.get('page', 1, type=int)
    per_page = 6
    # offset = (page-1) * per_page # THIS ISN'T REQUIRED WHEN WORKING WITH A PAGINATED QUERY OBJECT INSTEAD OF A LIST
    results = Result.query.filter_by(recipe_id = recipe_id).order_by(Result.created_at.desc()).paginate(page=page, per_page=per_page)
    total = Result.query.filter_by(recipe_id = recipe_id).count()
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    return render_template('recipe_read.html', title=recipe.name, recipe=recipe, result_form = result_form, results=results, pagination=pagination)


@recipes.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user != current_user:
        abort(403)
    db.session.delete(recipe)
    db.session.commit()
    flash('Your recipe has been deleted!', 'success')
    return redirect(url_for('main.home'))