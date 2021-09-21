from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

class ResultForm(FlaskForm):
    picture             = FileField('Recipe Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    snippet             = TextAreaField('Notes', validators=[DataRequired()], render_kw={"rows": 5})
    submit              = SubmitField('Submit')