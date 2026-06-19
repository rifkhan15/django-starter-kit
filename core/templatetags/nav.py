from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, menu_name_lower):
    resolver = context["request"].resolver_match
    view_class = getattr(resolver.func, "view_class", None)

    model = getattr(view_class, "model", None)

    request_name = (
        model._meta.model_name
        if model
        else resolver.view_name
    )

    return "active" if request_name == menu_name_lower else ""