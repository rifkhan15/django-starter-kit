from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, name):
    resolver = context["request"].resolver_match
    view_class = getattr(resolver.func, "view_class", None)

    model = getattr(view_class, "model", None)

    current = (
        model._meta.model_name
        if model
        else resolver.app_name
    )

    return "active" if current == name else ""