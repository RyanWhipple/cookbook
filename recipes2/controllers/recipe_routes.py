from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from recipes2 import db
from recipes2.models.recipe import Recipe
from recipes2.forms.recipe_forms import RecipeForm
from recipes2.utils.utils import save_picture

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
                picture_file = save_picture(form.picture.data)
            
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
    


@recipes.route('/recipe/<int:recipe_id>/update', methods=['GET', 'POST'])
@login_required
def update_recipe(recipe_id):
    form = RecipeForm()
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        abort(403)

    # Display form filled-in with Recipe's current data
    if request.method == 'GET':
        form.title.data = recipe.title
        form.short_description.data = recipe.short_description
        form.ingredients.data = recipe.ingredients
        form.directions.data = recipe.directions
        form.notes.data = recipe.notes
        return render_template('recipe_create_update.html', title='Update Recipe', form=form, legend='Update Recipe', recipe=recipe)

    # Save updated form
    elif request.method == "POST":
        if form.validate_on_submit():
            recipe.title = form.title.data
            recipe.short_description = form.short_description.data
            
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                recipe.image_file = picture_file
            
            recipe.directions = form.directions.data
            db.session.commit()
            flash('Your recipe has been updated!', 'success')
            return redirect(url_for('recipes.recipe', recipe_id=recipe.id))
    


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