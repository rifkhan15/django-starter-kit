from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, view_name):
    resolver = context['request'].resolver_match

    current_view_name = resolver.view_name

    return "active" if current_view_name == view_name else ""