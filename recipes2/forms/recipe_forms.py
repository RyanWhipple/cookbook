from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class RecipeForm(FlaskForm):
    name                = StringField('Name', validators=[DataRequired()], render_kw={"placeholder":"Recipe Name"})
    description         = StringField('Description', validators=[DataRequired()], render_kw={"placeholder":"Description"})
    picture             = FileField('Recipe Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    ingredients         = TextAreaField('Ingredients', validators=[DataRequired()], render_kw={"rows": 10})
    instructions        = TextAreaField('Instructions', validators=[DataRequired()], render_kw={"rows": 10})
    notes               = TextAreaField('Notes', validators=[DataRequired()], render_kw={"rows": 5})
    submit              = SubmitField('Submit')