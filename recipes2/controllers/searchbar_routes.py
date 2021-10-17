from flask import Blueprint
from flask import render_template, request
from recipes2 import db
from recipes2.models.recipe import Recipe
from recipes2.models.result import Result

searchbar = Blueprint("searchbar",__name__)

@searchbar.route('/search')
def search():
    search_query = request.args.get("q")
    search_by = "%{}%".format(search_query)
    results =[]
    results.push(Recipe.query.filter(Recipe.name.like(search_by)))
    results.push(Recipe.query.filter(Recipe.description.like(search_by)))
    results.push(Recipe.query.filter(Recipe.instructions.like(search_by)))
    results.push(Recipe.query.filter(Recipe.ingredients.like(search_by)))
    return render_template("search_page.html",results=results)
