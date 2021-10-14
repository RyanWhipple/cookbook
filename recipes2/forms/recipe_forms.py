from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, ValidationError

class RecipeForm(FlaskForm):
    name                = StringField('Name', validators=[DataRequired()], render_kw={"placeholder":"Recipe Name"})
    description         = StringField('Description', validators=[DataRequired()], render_kw={"placeholder":"Description"})
    prep_time           = StringField('Prep Time', validators=[DataRequired()])
    cook_time           = StringField('Cook Time', validators=[DataRequired()])
    picture             = FileField('Recipe Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    ingredients         = TextAreaField('Ingredients', validators=[DataRequired()], render_kw={"rows": 10})
    instructions        = TextAreaField('Instructions', validators=[DataRequired()], render_kw={"rows": 10})
    notes               = TextAreaField('Notes', validators=[DataRequired()], render_kw={"rows": 5})
    public              = BooleanField('Public',default="checked")
    submit              = SubmitField('Submit')

    def validate_prep_time(self, prep_time):
        if prep_time.data.isnumeric() == False:
            raise ValidationError('Prep times must be numbers')

    def validate_cook_time(self, cook_time):
        if cook_time.data.isnumeric() == False:
            raise ValidationError('Cook times must be numbers')