from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from recipes2 import db, login_manager
from flask import app
# from flask import current_app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id              = db.Column(db.Integer, primary_key=True)
    username        = db.Column(db.String(45), nullable=True)
    email           = db.Column(db.String(120), nullable=False, unique=True)
    password        = db.Column(db.String(60), nullable=False)
    created_at      = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at      = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    default_home    = db.Column(db.SmallInteger, nullable=False, default=0)
    default_privacy = db.Column(db.SmallInteger, nullable=False, default=3)
    first_name      = db.Column(db.String(45), nullable=True, default="")
    last_name       = db.Column(db.String(45), nullable=True, default="")
    image_file      = db.Column(db.String(20), nullable=False, default='default.jpg')
    recipes         = db.relationship(  'Recipe', backref='user',
                                    cascade="all, delete, delete-orphan", passive_deletes=True
                                    )

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        # s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        # s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
<<<<<<< Updated upstream
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
=======
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
>>>>>>> Stashed changes
