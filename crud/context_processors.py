from importlib import import_module
from django.apps import apps
from django.forms.models import BaseInlineFormSet
from .views import load_app_configs

#get module name of inlineformset (child model)
def get_inline_formset_models(app_label):
    result = {}

    try:
        forms_module = import_module(f"{app_label}.forms")
    except ModuleNotFoundError:
        return result

    for obj in vars(forms_module).values():

        if (
            isinstance(obj, type)
            and issubclass(obj, BaseInlineFormSet)
            and hasattr(obj, "fk")
            and hasattr(obj, "model")
        ):
            parent_model = obj.fk.remote_field.model
            child_model = obj.model

            result[parent_model.__name__] = child_model

    return result

#expose th module name of inlineformset (child model) which was got from code abov
def formset_labels(request):

    resolver = getattr(request, "resolver_match", None)

    if not resolver:
        return {}

    try:
        app_label, model_name, _ = resolver.url_name.split("_")
    except (AttributeError, ValueError):
        return {}

    formsets = get_inline_formset_models(app_label)

    child_model = formsets.get(model_name)

    if not child_model:
        return {}

    return {
        "formset_verbose_name": child_model._meta.verbose_name,
        "formset_verbose_name_plural": child_model._meta.verbose_name_plural,
    }

#generate list of nav items using model list on app_configs.
def crud_menu(request):
    menu = []

    configs = load_app_configs()

    excluded_models = set()

    # collect child models managed by inline formsets
    for app_name in configs.keys():

        formsets = get_inline_formset_models(app_name)

        for child_model in formsets.values():
            excluded_models.add(child_model.__name__)

    # build menu
    for app_name, config in configs.items():

        for model_name in config["model_names"]:

            if model_name in excluded_models:
                continue

            model = apps.get_model(app_name, model_name)

            menu.append({
                "app_name": app_name.title(),
                "model_title": model._meta.verbose_name_plural.title(),
                "list_url": f"{app_name}_{model_name}_list",
            })

    return {
        "crud_menu": menu,
    }