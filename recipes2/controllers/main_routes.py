from flask import Blueprint
from flask import render_template, request
from sqlalchemy.sql.elements import or_
from recipes2.models.recipe import Recipe
from recipes2.forms.recipe_forms import RecipeForm
from recipes2.forms.result_forms import ResultForm
from recipes2.utils.utils import save_picture
from flask_login import current_user
from flask_paginate import Pagination


main = Blueprint('main', __name__)

@main.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 6
    # offset = (page-1) * per_page # THIS ISN'T REQUIRED WHEN WORKING WITH A PAGINATED QUERY OBJECT INSTEAD OF A LIST
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).filter(or_(Recipe.public==1,(current_user.is_authenticated and Recipe.user == current_user))).paginate(page=page, per_page=per_page)
    total = Recipe.query.count()
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    return render_template('home.html', title='Home', recipes=recipes, pagination = pagination)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/ajax/image/update/<folder>', methods=['POST'])
def update_image(folder):
    if folder=="recipe_pics":
        form=RecipeForm()
    if folder=="result_pics":
        form=ResultForm()
    picture=form.picture.data
    return save_picture(picture,folder)