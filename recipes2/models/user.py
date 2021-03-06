from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from recipes2 import db, login_manager
from flask import app
import os
# from flask import current_app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Follower must be defined first since it is used as part of the definition of a User
class Follower(db.Model):
    __tablename__ = "follower"
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followee_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)


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
    results         = db.relationship(  'Result', backref='user',
                                    cascade="all, delete, delete-orphan", passive_deletes=True
                                    )

    follower_id      = db.relationship('Follower', backref='follower', primaryjoin=id==Follower.follower_id)
    followee_id      = db.relationship('Follower', backref='followee', primaryjoin=id==Follower.followee_id)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(os.environ['SECRET_KEY'], expires_sec)
        # s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(os.environ['SECRET_KEY'])
        # s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"