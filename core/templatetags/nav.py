from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, model_name):
    resolver = context['request'].resolver_match

    view_class = getattr(resolver.func, "view_class", None)
    if not view_class:
        return ""

    current_model_name = view_class.model._meta.model_name
    return "active" if current_model_name == model_name else ""