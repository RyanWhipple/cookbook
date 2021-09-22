from flask import Blueprint
from flask import render_template, request
from recipes2.models.recipe import Recipe
from recipes2.forms.recipe_forms import RecipeForm
from recipes2.utils.utils import save_picture


main = Blueprint('main', __name__)

@main.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).paginate(page=page, per_page=6)
    return render_template('home.html', title='Home', recipes=recipes)


@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/ajax/image/update/<folder>', methods=['POST'])
def update_image(folder):
    print(type(folder))
    if folder=="recipe_pics":
        form=RecipeForm()
    picture=form.picture.data
    return save_picture(picture,folder)