#make an app_config.py file for each new crud app and include the below code. define the app name, model names and extra view.context.

APP_CONFIG = {
    "model_names": ["Order", "Customer"],
    "extra_context": {
        "view.context_a": "value_a",
        "view.context_b": "value_b",
    }
}