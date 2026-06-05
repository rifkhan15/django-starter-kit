from .autocrud import load_app_configs
from django.apps import apps

def crud_menu(request):

    menu = []

    configs = load_app_configs()

    for app_name, config in configs.items():

        for model_name in config["model_names"]:

            model = apps.get_model(app_name, model_name)

            menu.append({
                "app_name": app_name.title(),
                "model_title": model._meta.verbose_name_plural.title(),
                "list_url": f"{app_name}_{model_name}_list",
                # "create_url": f"{app_name}_{model_name}_create",
            })

    return {"crud_menu": menu}