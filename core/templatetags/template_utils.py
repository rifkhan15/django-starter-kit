from django import template
from django.template.loader import select_template

register = template.Library()


@register.simple_tag
def existing_template(*templates):
    return select_template(templates).template.name