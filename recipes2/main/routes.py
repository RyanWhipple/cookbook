from flask import Blueprint
from flask import render_template, request
from recipes2.models import Recipe

main = Blueprint('main', __name__)

@main.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.order_by(Recipe.date_posted.desc()).paginate(page=page, per_page=6)
    return render_template('home.html', title='Home', recipes=recipes)


@main.route('/about')
def about():
    return render_template('about.html')