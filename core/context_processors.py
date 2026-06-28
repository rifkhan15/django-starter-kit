from core.config_loader import load_app_configs

def crud_menu(request):
    crud_menu = []

    for app_label, config in load_app_configs().items():

        nav_excludes = config.get("nav_excludes", {})

        for model in config["crud_models"]:

            # skip excluded models
            if model in nav_excludes:
                continue

            crud_menu.append({
                "model_name": model._meta.model_name,
                "model_title": model._meta.verbose_name_plural.title(),
                "url": f"{app_label.lower()}{model._meta.model_name}_list",
            })

    return {
        "crud_menu": crud_menu
    }