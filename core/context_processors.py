from core.config_loader import load_app_configs

def crud_menu(request):
    crud_menu = []

    configs = load_app_configs()

    for app_label, config in configs.items():

        nav_hidden = config.get("nav_hidden", [])

        for model in config["crud_models"]:

            # skip hidden models
            if model in nav_hidden:
                continue

            crud_menu.append({
                "model_name": model._meta.model_name,
                "model_title": model._meta.verbose_name_plural.title(),
                "url": f"{app_label.lower()}{model._meta.model_name}_list",
            })

    return {
        "crud_menu": crud_menu
    }