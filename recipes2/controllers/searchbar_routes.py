from flask import Blueprint
from flask import render_template, request
from flask_login import current_user
from recipes2 import db
from recipes2.models.recipe import Recipe
from flask_paginate import Pagination, get_page_parameter


searchbar = Blueprint("searchbar",__name__)

@searchbar.route('/search', methods=["GET"])
def search():
    # search by the get request
    search_query = request.args.get("q")
    search_by = "%{}%".format(search_query)
    results =list(Recipe.query.filter(Recipe.name.like(search_by))) +\
    list(Recipe.query.filter(Recipe.description.like(search_by))) +\
    list(Recipe.query.filter(Recipe.ingredients.like(search_by))) +\
    list(Recipe.query.filter(Recipe.instructions.like(search_by)))
    # get only public recipes
    filtered = list(filter(lambda result: result.public == 1 or (current_user.is_authenticated and current_user.id == result.user_id), results))
    # remove duplicates from list
    filtered = list(set(filtered))
    #if user is logged in show the recipes of users they are following first
    if current_user.is_authenticated:
        following = [ _.followee_id for _ in current_user.follower_id]
        filtered.sort(key=lambda x: 0 if x.user_id in following else 1)
    # pagination was copied and pasted from social feed
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 6
    offset = (page-1) * per_page
    total = len(filtered)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    filtered = filtered[offset : offset + per_page]
    return render_template("search_page.html",recipes=filtered,
                            page=page,
                            per_page=per_page,
                            pagination=pagination,
                            title="Search Recipes",
                            query=search_query)

@searchbar.route('/ajax/search', methods=["GET"])
def ajax_search():
    # search by the get request
    search_query = request.args.get("q")
    search_by = "%{}%".format(search_query)
    results =list(Recipe.query.filter(Recipe.name.like(search_by))) +\
    list(Recipe.query.filter(Recipe.description.like(search_by))) +\
    list(Recipe.query.filter(Recipe.ingredients.like(search_by))) +\
    list(Recipe.query.filter(Recipe.instructions.like(search_by)))
    # get only public recipes
    filtered = list(filter(lambda result: result.public == 1 or (current_user.is_authenticated and current_user.id == result.user_id), results))
    # remove duplicates from list
    filtered = list(set(filtered))
    #if user is logged in show the recipes of users they are following first
    if current_user.is_authenticated:
        following = [ _.followee_id for _ in current_user.follower_id]
        filtered.sort(key=lambda x: 0 if x.user_id in following else 1)
    # pagination was copied and pasted from social feed
    page = request.args.get(get_page_parameter(), type=int, default=1)
    print(page)
    per_page = 6
    offset = (page-1) * per_page
    total = len(filtered)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4',href=f"/search?q={search_query}&page={'{0}'}")
    filtered = filtered[offset : offset + per_page]
    return render_template("partials/search.html",recipes=filtered,
                            page=page,
                            per_page=per_page,
                            pagination=pagination
                            )
