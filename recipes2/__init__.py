import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
# from recipes2.config import Config

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']

# iCloud Email
app.config['MAIL_SERVER'] = 'smtp.mail.me.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ['EMAIL_USER']
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASS']

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = "info"
mail = Mail(app)

from recipes2.controllers.users import users
app.register_blueprint(users)

from recipes2.controllers.recipes import recipes
app.register_blueprint(recipes)

from recipes2.controllers.main_routes import main
app.register_blueprint(main)

from recipes2.controllers.error_handlers import errors
app.register_blueprint(errors)



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