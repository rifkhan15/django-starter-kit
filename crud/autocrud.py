# crud/autocrud.py

from django.apps import apps
from django.urls import path
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from importlib import import_module

urlpatterns = []


def load_app_configs():
    configs = {}

    for app in apps.get_app_configs():
        try:
            module = import_module(f"{app.name}.app_config")
            configs[app.label] = module.APP_CONFIG
        except Exception:
            continue

    return configs


def make_views(model, app_label, extra_context):

    class BaseMixin:
        extra_context = extra_context or {}

    class L(BaseMixin, ListView):
        model = model

    class D(BaseMixin, DetailView):
        model = model

    class C(BaseMixin, CreateView):
        model = model
        fields = "__all__"

        def get_success_url(self):
            return f"/{app_label.lower()}/"

    class U(BaseMixin, UpdateView):
        model = model
        fields = "__all__"

        def get_success_url(self):
            return f"/{app_label.lower()}/"

    class X(BaseMixin, DeleteView):
        model = model

        def get_success_url(self):
            return f"/{app_label.lower()}/"

    return L, D, C, U, X


def generate():
    configs = load_app_configs()

    global urlpatterns

    for app_label, config in configs.items():

        for model_name in config["model_names"]:

            model = apps.get_model(app_label, model_name)

            ListV, DetailV, CreateV, UpdateV, DeleteV = make_views(
                model,
                app_label,
                config.get("extra_context"),
            )

            base = f"{app_label.lower()}/{model_name.lower()}"

            urlpatterns += [
                path(f"{base}/", ListV.as_view()),
                path(f"{base}/<int:pk>/", DetailV.as_view()),
                path(f"{base}/create/", CreateV.as_view()),
                path(f"{base}/<int:pk>/update/", UpdateV.as_view()),
                path(f"{base}/<int:pk>/delete/", DeleteV.as_view()),
            ]