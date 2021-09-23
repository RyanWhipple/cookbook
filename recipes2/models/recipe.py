from datetime import datetime
from recipes2 import db
# from flask import current_app

class Recipe(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(155))
    image_file          = db.Column(db.String(20), nullable=False, default='default.jpg')
    description         = db.Column(db.String(255))
    cook_time           = db.Column(db.Integer)
    prep_time           = db.Column(db.Integer)
    instructions        = db.Column(db.Text)
    ingredients         = db.Column(db.Text)
    notes               = db.Column(db.Text)
    public              = db.Column(db.SmallInteger)
    created_at          = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at          = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id             = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"Recipe('{self.name}', '{self.user_id}, '{self.created_at}')"
