import re
from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from recipes2 import db
import recipes2
from recipes2.models.recipe import Recipe
from recipes2.models.result import Result
from recipes2.models.user import Follower
from recipes2.forms.recipe_forms import RecipeForm
from recipes2.forms.result_forms import ResultForm
from recipes2.utils.utils import save_picture
from sqlalchemy import delete

from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import create_engine


social_feeds = Blueprint('social_feed', __name__)


# See https://gist.github.com/mozillazg/69fb40067ae6d80386e10e105e6803c9
# See https://pythonhosted.org/Flask-paginate/
@social_feeds.route('/social_feed/', methods=['GET', 'POST'])
@login_required
def social_feed():
    
    
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).filter_by(public=1)
    results = Result.query.order_by(Result.created_at.desc()).filter(Result.recipe_id.in_([recipe.id for recipe in recipes]))
    following = [ _.followee_id for _ in current_user.follower_id]
    # print("recipes: ", recipes)
    result_list = [ _ for _ in recipes]+[ _ for _ in results]
    result_list.sort(key=lambda x: x.created_at, reverse=True)
    print(result_list)
    


    items_to_show = []
    recipe_index = 0
    result_index = 0
    num_of_recipes = recipes.count()
    num_of_results = results.count()
    recipes_left = num_of_recipes > 0
    results_left = num_of_results > 0
    
    while len(items_to_show) < 10:
        if results_left and results[result_index].created_at > recipes[recipe_index].created_at:
            items_to_show.append([results[result_index], "result"])
            result_index += 1
            if result_index == num_of_results:
                print("Ran out of results!")
                results_left = False
        elif recipes_left:
            items_to_show.append([recipes[recipe_index], "recipe"])
            recipe_index += 1
            if recipe_index == num_of_recipes:
                print("Ran out of recipes!")
                recipes_left = False
        if not recipes_left and not results_left:
            print("Ran out of both results and recipes!")
            break

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 5
    offset = (page-1) * per_page
    total = len(items_to_show)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    items_to_show = items_to_show[offset : offset + per_page]

    
    
    return render_template('social_feed.html',
                            items_to_show = items_to_show,
                            page=page,
                            per_page=per_page,
                            pagination=pagination,
                            title="Social Feed"
                            )


@social_feeds.route('/social_feed/follow/<int:followee_id>', methods=['GET', 'POST'])
@login_required
def follow(followee_id):
    
    follower = Follower(follower_id=current_user.id, followee_id=followee_id)
    db.session.add(follower)
    db.session.commit()
    
    return redirect(url_for('main.home'))


@social_feeds.route('/social_feed/unfollow/<int:followee_id>', methods=['GET', 'POST'])
@login_required
def unfollow(followee_id):
    
    to_delete = Follower.query.filter(Follower.followee_id==followee_id, Follower.follower_id == current_user.id).first()
    db.session.delete(to_delete)
    db.session.commit()
    
    return redirect(url_for('users.account'))


@social_feeds.route('/social_feed/block/<int:follower_id>', methods=['GET', 'POST'])
@login_required
def block(follower_id):
    
    to_delete = Follower.query.filter(Follower.follower_id==follower_id, Follower.followee_id == current_user.id).first()
    db.session.delete(to_delete)
    db.session.commit()
    
    return redirect(url_for('users.account'))