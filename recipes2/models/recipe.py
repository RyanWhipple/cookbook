from datetime import datetime
from recipes2 import db
# from flask import current_app

class Recipe(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    title               = db.Column(db.String(100), nullable=False)
    short_description   = db.Column(db.String(255), nullable=False)
    image_file          = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_posted         = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ingredients         = db.Column(db.Text, nullable=False)
    directions          = db.Column(db.Text, nullable=False)
    notes               = db.Column(db.Text, nullable=False)
    user_id             = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"