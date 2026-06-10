from django.apps import apps
from importlib import import_module

# ---------------------------
# LOAD APP CONFIGS
# ---------------------------
def load_app_configs():
    configs = {}

    for app in apps.get_app_configs():
        try:
            module = import_module(f"{app.name}.app_config")
            configs[app.label] = module.APP_CONFIG
        except ImportError:
            pass

    return configs