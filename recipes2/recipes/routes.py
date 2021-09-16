from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from recipes2 import db
from recipes2.models import Recipe
from recipes2.recipes.forms import RecipeForm
from recipes2.users.utils import save_picture

recipes = Blueprint('recipes', __name__)

@recipes.route('/recipe/new', methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        
        # if form.picture.data:
        print("Before saving picture")
        picture_file = save_picture(form.picture.data)
        print("picture_file: ", picture_file)
        
        recipe = Recipe(title               = form.title.data,
                        short_description   = form.short_description.data,
                        image_file          = picture_file,
                        ingredients         = form.ingredients.data,
                        directions          = form.directions.data,
                        notes               = form.notes.data,
                        author              = current_user)
        db.session.add(recipe)
        db.session.commit()
        flash('Your recipe has been created!','success')
        return redirect(url_for('main.home'))
    return render_template('recipe_create_update.html', title='New Recipe', form=form, legend='New Recipe')


@recipes.route('/recipe/<int:recipe_id>/update', methods=['GET', 'POST'])
@login_required
def update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        abort(403)
    form = RecipeForm()
    print("Update Route form:", form)
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.short_description = form.short_description.data
        
        # if form.picture.data:
        print("Before saving picture")
        picture_file = save_picture(form.picture.data)
        print("picture_file: ", picture_file)
        recipe.image_file = picture_file
        
        recipe.directions = form.directions.data
        db.session.commit()
        flash('Your recipe has been updated!', 'success')
        return redirect(url_for('recipes.recipe', recipe_id=recipe.id))
    elif request.method == 'GET':
        form.title.data = recipe.title
        form.short_description.data = recipe.short_description
        form.directions.data = recipe.directions
    return render_template('recipe_create_update.html', title='Update Recipe', form=form, legend='Update Recipe')


@recipes.route('/recipe/<int:recipe_id>', methods=['GET', 'POST'])
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe_read.html', title=recipe.title, recipe=recipe)


@recipes.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        abort(403)
    db.session.delete(recipe)
    db.session.commit()
    flash('Your recipe has been deleted!', 'success')
    return redirect(url_for('main.home'))