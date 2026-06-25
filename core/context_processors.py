from django.apps import apps
from core.config_loader import load_app_configs

def crud_menu(request):
    crud_menu = []

    for app_label, config in load_app_configs().items():
        nav_excludes = config.get("nav_excludes", [])

        for crud_model in config["crud_models"]:
            if crud_model in nav_excludes:
                continue

            model = apps.get_model(app_label, crud_model)

            crud_menu.append({
                "model_name": model._meta.model_name,
                "model_title": model._meta.verbose_name_plural.title(),
                "url": f"{app_label}_{model._meta.model_name}_list",
            })

    return {
        "crud_menu": crud_menu
    }