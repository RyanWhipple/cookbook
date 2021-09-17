import re

from flask import Blueprint
from jinja2 import evalcontextfilter, Markup, escape

custom_template_filers = Blueprint('custom_template_filters', __name__)

@evalcontextfilter
@custom_template_filers.app_template_filter()
def newline_to_br(context, value: str) -> str:
    result = "<br />".join(re.split(r'(?:\r\n|\r|\n){2,}', escape(value)))

    if context.autoescape:
        result = Markup(result)

    return result