from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    short_description = StringField('Short Description', validators=[DataRequired()])
    picture = FileField('Recipe Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')