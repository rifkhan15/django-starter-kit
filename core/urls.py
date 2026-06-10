
from django.urls import path
from django.apps import apps
from core.config_loader import load_app_configs
from core.views import make_views

core_urlpatterns = []

def generate_core_urls():
    global core_urlpatterns

    configs = load_app_configs()

    for app_label, config in configs.items():

        for model_name in config["model_names"]:

            model = apps.get_model(app_label, model_name)

            ListV, DetailV, CreateV, UpdateV, DeleteV = make_views(
                model=model,
                app_label=app_label,
                model_name=model_name,
            )

            base = f"{app_label.lower()}/{model_name.lower()}"

            core_urlpatterns += [
                path(f"{base}/", ListV.as_view(),
                     name=f"{app_label}_{model_name}_list"),

                path(f"{base}/create/", CreateV.as_view(),
                     name=f"{app_label}_{model_name}_create"),

                path(f"{base}/<int:pk>/", DetailV.as_view(),
                     name=f"{app_label}_{model_name}_detail"),

                path(f"{base}/<int:pk>/update/", UpdateV.as_view(),
                     name=f"{app_label}_{model_name}_update"),

                path(f"{base}/<int:pk>/delete/", DeleteV.as_view(),
                     name=f"{app_label}_{model_name}_delete"),
            ]