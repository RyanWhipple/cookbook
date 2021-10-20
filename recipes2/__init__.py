import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
# from recipes2.config import Config

app = Flask(__name__)

# RESTART VIRTUAL ENVIRONMENT IF CHANGING FROM HARDCODED VALUE TO AN os.environ VALUE

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

# Database Connection config:
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']


# iCloud Email
mail_settings={
    'MAIL_SERVER':'smtp.gmail.com',
    'MAIL_USE_TLS':False,
    'MAIL_USE_SLL':True,
    'MAIL_PORT':465,
    'MAIL_USERNAME':os.environ['EMAIL_USER'],
    'MAIL_PASSWORD':os.environ['EMAIL_PASS']
}
app.config.update(mail_settings)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = "info"
mail = Mail(app)

from recipes2.controllers.user_routes import users
app.register_blueprint(users)

from recipes2.controllers.recipe_routes import recipes
app.register_blueprint(recipes)

from recipes2.controllers.result_routes import results
app.register_blueprint(results)

from recipes2.controllers.main_routes import main
app.register_blueprint(main)

from recipes2.controllers.error_handlers import errors
app.register_blueprint(errors)

from recipes2.controllers.social_feed_routes import social_feeds
app.register_blueprint(social_feeds)

from recipes2.utils.custom_template_filters import custom_template_filters
app.register_blueprint(custom_template_filters)

from recipes2.controllers.searchbar_routes import searchbar
app.register_blueprint(searchbar)

# SQLite code
# This code block is necessary to make ondelete="cascade" work
# from https://stackoverflow.com/a/62327279

# from sqlalchemy import event
# from sqlalchemy.engine import Engine
# from sqlite3 import Connection as SQLite3Connection

# @event.listens_for(Engine, "connect")
# def _set_sqlite_pragma(dbapi_connection, connection_record):
#     if isinstance(dbapi_connection, SQLite3Connection):
#         cursor = dbapi_connection.cursor()
#         cursor.execute("PRAGMA foreign_keys=ON;")
#         cursor.close()




# This code block is for connecting to MySQL
# https://hackersandslackers.com/python-database-management-sqlalchemy/

# from sqlalchemy import create_engine

# engine=create_engine(
#     "mysql+pymysql://root:theverybest@127.0.0.1:3306/recipes2"
# )

# Might need to be db.engine???
# https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91
# db.engine=create_engine(
#     "mysql+pymysql://root:theverybest@127.0.0.1:3306/recipes2"
# )


#  ###
#  Code below is to use a factory to build the app based on the config file.  This didn't work well with SQLite because the db couldn't be initialized without the app running since the app only created the DB once it was initialized with the config file
#  Might re-instate this now that we're on MySQL but there is no rush to do so.
#  ###

# db = SQLAlchemy()
# bcrypt = Bcrypt()
# login_manager = LoginManager()
# login_manager.login_view = 'users.login'
# login_manager.login_message_category = "info"
# mail = Mail()


# def create_app(config_class=Config):
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     db.init_app(app)
#     bcrypt.init_app(app)
#     login_manager.init_app(app)
#     mail.init_app(app)

#     from recipes2.users.routes import users
#     app.register_blueprint(users)

#     from recipes2.recipes.routes import recipes
#     app.register_blueprint(recipes)

#     from recipes2.main.routes import main
#     app.register_blueprint(main)

#     from recipes2.errors.handlers import errors
#     app.register_blueprint(errors)

#     return app