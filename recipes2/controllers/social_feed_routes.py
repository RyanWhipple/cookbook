from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from recipes2 import db
from recipes2.models.recipe import Recipe
from recipes2.models.result import Result
from recipes2.models.user import Follower
from recipes2.forms.recipe_forms import RecipeForm
from recipes2.forms.result_forms import ResultForm
from recipes2.utils.utils import save_picture
from sqlalchemy import delete


social_feeds = Blueprint('social_feed', __name__)

@social_feeds.route('/social_feed/', methods=['GET', 'POST'])
@login_required
def social_feed():
    
    recipes = Recipe.query.order_by(Recipe.created_at.desc())
    results = Result.query.order_by(Result.created_at.desc())
    
    print("recipes: ", recipes)

    items_to_show = []
    recipe_index = 0
    result_index = 0
    recipes_left = True
    results_left = True
    num_of_recipes = recipes.count()
    num_of_results = results.count()
    

    

    while len(items_to_show) < 24:
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

    print("items_to_show: ", items_to_show)

    return render_template('social_feed.html', title='Social_Feed', items_to_show=items_to_show)


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