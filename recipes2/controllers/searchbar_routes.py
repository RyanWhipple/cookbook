from flask import Blueprint
from flask import render_template, request
from recipes2 import db
from recipes2.models.recipe import Recipe
from recipes2.models.result import Result

searchbar = Blueprint("searchbar",__name__)

@app.route('/search')
def search():
    search_query = request.args.get("q")
    search_by = "%{}%".format(search_query)
    results = Recipe.query.filter(Recipe.description.like(search_by)).all()
    return render_template("search_page.html",results=results)
