from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from recipes2 import db
from recipes2.models.result import Result
from recipes2.forms.result_forms import ResultForm
from recipes2.utils.utils import save_picture

results = Blueprint('results', __name__)

# Route is no longer used, superceded by AJAX-based create_result()
@results.route('/recipe/<int:recipe_id>/result/new', methods=['GET', 'POST'])
@login_required
def new_result(recipe_id):
    form = ResultForm()
    
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
            return redirect (url_for('recipes.recipe', recipe_id=recipe_id))
        else:
            print("new_recipe form.validate_on_submit() failed")

@results.route('/recipe/<int:recipe_id>/ajax/results/create', methods=['POST'])
def create_result(recipe_id):
    form = ResultForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, "result_pics/")
        result = Result(image_file          = picture_file,
                        snippet             = form.snippet.data,
                        recipe_id           = recipe_id,
                        user_id             = current_user.id)
        db.session.add(result)
        db.session.commit()
        return render_template('partials/result.html',result = result)
    else:
        print("new_recipe form.validate_on_submit() failed")
        return ""