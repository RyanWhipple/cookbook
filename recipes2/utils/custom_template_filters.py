import re

from flask import Blueprint
from jinja2 import evalcontextfilter, Markup, escape

custom_template_filters = Blueprint('custom_template_filters', __name__)

@evalcontextfilter
@custom_template_filters.app_template_filter()
def newline_to_br(context, value: str) -> str:
    result = "<br />".join(re.split(r'(?:\r\n|\r|\n){2,}', escape(value)))

    if context.autoescape:
        result = Markup(result)

    return result

@evalcontextfilter
@custom_template_filters.app_template_filter()
def ordinal_date(context, value: str) -> str:
    
    print("value: ", value)

    date_suffix = ["th", "st", "nd", "rd"]

    v = int(value) % 10
    if v in [1, 2, 3] and value not in [11, 12, 13]:
        return date_suffix[v]
    else:
        return date_suffix[0]