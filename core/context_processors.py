from django.apps import apps
from core.config_loader import load_app_configs

def crud_menu(request):
    crud_menu = []

    for app_label, config in load_app_configs().items():
        nav_exclude = config.get("nav_exclude", [])

        for modelclass_name in config["modelclass_names"]:
            if modelclass_name in nav_exclude:
                continue

            model = apps.get_model(app_label, modelclass_name)

            crud_menu.append({
                "model_name": model._meta.model_name,
                "model_title": model._meta.verbose_name_plural.title(),
                "url": f"{app_label}_{model._meta.model_name}_list",
            })

    return {
        "crud_menu": crud_menu
    }