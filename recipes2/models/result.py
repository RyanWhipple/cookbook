from datetime import datetime
from recipes2 import db
# from flask import current_app

class Result(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    user_id             = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    recipe_id           = db.Column(db.Integer, db.ForeignKey('recipe.id', ondelete="CASCADE"), nullable=False)
    snippet             = db.Column(db.String(150), nullable=True)
    image_file          = db.Column(db.String(20), nullable=False, default='default.jpg')
    created_at          = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at          = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    
    
    def __repr__(self):
        return f"Result('{self.snippet}', '{self.user_id}', '{self.created_at}')"