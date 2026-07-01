from django.urls import path
from core.config_loader import load_app_configs
from core.views import make_views

core_urlpatterns = []

def generate_core_urls():
    global core_urlpatterns

    configs = load_app_configs()

    for config in configs.values():

        for model in config["crud_models"]:

            app_label = model._meta.app_label
            model_name = model._meta.model_name

            (ListV, DetailV, CreateV, UpdateV, DeleteV) = make_views(
                model=model,
            )

            basepath = (f"{app_label.lower()}/"f"{model_name}")
            basename = (f"{app_label.lower()}"f"{model_name}")

            core_urlpatterns += [
                path(f"{basepath}/", ListV.as_view(), name=f"{basename}_list"),
                path(f"{basepath}/create/", CreateV.as_view(), name=f"{basename}_create"),
                path(f"{basepath}/<int:pk>/", DetailV.as_view(), name=f"{basename}_detail"),
                path(f"{basepath}/<int:pk>/update/", UpdateV.as_view(), name=f"{basename}_update"),
                path(f"{basepath}/<int:pk>/delete/", DeleteV.as_view(), name=f"{basename}_delete")
            ]