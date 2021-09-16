from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class RecipeForm(FlaskForm):
    title               = StringField('Title', validators=[DataRequired()], render_kw={"placeholder":"Recipe Title"})
    short_description   = StringField('Short Description', validators=[DataRequired()], render_kw={"placeholder":"Short Description"})
    picture             = FileField('Recipe Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    ingredients         = TextAreaField('Ingredients', validators=[DataRequired()], render_kw={"rows": 10})
    directions          = TextAreaField('Directions', validators=[DataRequired()], render_kw={"rows": 10})
    notes               = TextAreaField('Notes', validators=[DataRequired()], render_kw={"rows": 5})
    submit              = SubmitField('Submit')