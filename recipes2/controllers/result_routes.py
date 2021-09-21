from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from recipes2 import db
from recipes2.models.result import Result
from recipes2.forms.result_forms import ResultForm
from recipes2.utils.utils import save_picture

results = Blueprint('results', __name__)

@results.route('/recipe/<int:recipe_id>/result/new', methods=['GET', 'POST'])
@login_required
def new_result(recipe_id):
    form = ResultForm()

    # NOT REQUIRED FOR MODAL FORMS ?????
    # # Display Blank Form
    # if request.method == "GET":
    #     return render_template('recipe_create_update.html', title='New Recipe', form=form, legend='New Recipe')
    
    # Save Filled-in Form
    if request.method == "POST":
        if form.validate_on_submit():
            
            if form.picture.data:
                picture_file = save_picture(form.picture.data, "result_pics/")
            
            result = Result(image_file          = picture_file,
                            snippet             = form.snippet.data,
                            recipe_id           = recipe_id,
                            user_id             = current_user.id)
            db.session.add(result)
            db.session.commit()
            flash('Your result has been created!','success')
            return redirect(f'/recipe/{recipe_id}')
        else:
            print("new_recipe form.validate_on_submit() failed")
#             # return render_template('recipe_create_update.html', title='New Recipe', form=form, legend='New Recipe')

    


# @recipes.route('/recipe/<int:recipe_id>/update', methods=['GET', 'POST'])
# @login_required
# def update_recipe(recipe_id):
#     form = RecipeForm()
#     recipe = Recipe.query.get_or_404(recipe_id)
#     if recipe.user != current_user:
#         abort(403)

#     # Display form filled-in with Recipe's current data
#     if request.method == 'GET':
#         form.name.data          = recipe.name
#         form.description.data   = recipe.description
#         form.prep_time.data     = recipe.prep_time
#         form.cook_time.data     = recipe.cook_time
#         form.ingredients.data   = recipe.ingredients
#         form.instructions.data  = recipe.instructions
#         form.notes.data         = recipe.notes
#         return render_template('recipe_create_update.html', title='Update Recipe', form=form, legend='Update Recipe', recipe=recipe)

#     # Save updated form
#     elif request.method == "POST":
#         if form.validate_on_submit():
#             recipe.name         = form.name.data
#             recipe.description  = form.description.data
#             recipe.prep_time    = form.prep_time.data
#             recipe.cook_time    = form.cook_time.data
            
#             if form.picture.data:
#                 picture_file = save_picture(form.picture.data, "recipe_pics/")
#                 recipe.image_file = picture_file
            
#             recipe.ingredients  = form.ingredients.data
#             recipe.instructions = form.instructions.data
#             recipe.notes        = form.notes.data
#             db.session.commit()
#             flash('Your recipe has been updated!', 'success')
#             return redirect(url_for('recipes.recipe', recipe_id=recipe.id))
#         else:
#             print("update_recipe form.validate_on_submit() failed")
#             return render_template('recipe_create_update.html', title=recipe.name, form=form, legend=recipe.name)
    


# @recipes.route('/recipe/<int:recipe_id>', methods=['GET', 'POST'])
# def recipe(recipe_id):
#     recipe = Recipe.query.get_or_404(recipe_id)
#     return render_template('recipe_read.html', title=recipe.name, recipe=recipe)


# @recipes.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
# @login_required
# def delete_recipe(recipe_id):
#     recipe = Recipe.query.get_or_404(recipe_id)
#     if recipe.user != current_user:
#         abort(403)
#     db.session.delete(recipe)
#     db.session.commit()
#     flash('Your recipe has been deleted!', 'success')
#     return redirect(url_for('main.home'))