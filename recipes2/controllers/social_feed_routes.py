import re
from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from recipes2 import db
from datetime import datetime,timedelta
from recipes2.models.recipe import Recipe
from recipes2.models.result import Result
from recipes2.models.user import Follower
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
    items_to_show = [ _ for _ in recipes]+[ _ for _ in results]
    items_to_show.sort(key=lambda x: x.created_at, reverse=True)
    items_to_show.sort(key=lambda x: 0 if (x.user_id in following and datetime.now() - x.created_at < timedelta(days=3)) else 1)    

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