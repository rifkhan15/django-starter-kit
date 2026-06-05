from importlib import import_module

from django.apps import apps
from django.urls import path
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

crud_urlpatterns = []


def load_app_configs():
    configs = {}

    for app in apps.get_app_configs():
        try:
            module = import_module(f"{app.name}.app_config")
            configs[app.label] = module.APP_CONFIG
        except ImportError:
            pass

    return configs


def make_views(
    *,
    model,
    app_label,
    model_name,
):

    class ContextMixin:
        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)

            ctx["app_label"] = app_label
            ctx["model_name"] = model_name
            ctx["model_verbose_name"] = model._meta.verbose_name
            ctx["model_title"] = model._meta.verbose_name_plural.title()
            
            ctx["list_url"] = f"{app_label}_{model_name}_list"
            ctx["create_url"] = f"{app_label}_{model_name}_create"
            ctx["detail_url"] = f"{app_label}_{model_name}_detail"
            ctx["update_url"] = f"{app_label}_{model_name}_update"
            ctx["delete_url"] = f"{app_label}_{model_name}_delete"

            return ctx

    class L(ContextMixin, ListView):
        template_name = "list.html"

    L.model = model

    class D(ContextMixin, DetailView):
        template_name = "detail.html"

    D.model = model

    class C(ContextMixin, CreateView):
        fields = "__all__"
        template_name = "create.html"

        def get_success_url(self):
            return f"/{app_label.lower()}/{model_name.lower()}/"

    C.model = model

    class U(ContextMixin, UpdateView):
        fields = "__all__"
        template_name = "update.html"

        def get_success_url(self):
            return f"/{app_label.lower()}/{model_name.lower()}/"

    U.model = model

    class X(ContextMixin, DeleteView):
        template_name = "confirm_delete.html"

        def get_success_url(self):
            return f"/{app_label.lower()}/{model_name.lower()}/"

    X.model = model

    return L, D, C, U, X


def generate():
    global crud_urlpatterns

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

            crud_urlpatterns.extend(
                [
                    path(
                        f"{base}/",
                        ListV.as_view(),
                        name=f"{app_label}_{model_name}_list",
                    ),
                    path(
                        f"{base}/create/",
                        CreateV.as_view(),
                        name=f"{app_label}_{model_name}_create",
                    ),
                    path(
                        f"{base}/<int:pk>/",
                        DetailV.as_view(),
                        name=f"{app_label}_{model_name}_detail",
                    ),
                    path(
                        f"{base}/<int:pk>/update/",
                        UpdateV.as_view(),
                        name=f"{app_label}_{model_name}_update",
                    ),
                    path(
                        f"{base}/<int:pk>/delete/",
                        DeleteV.as_view(),
                        name=f"{app_label}_{model_name}_delete",
                    ),
                ]
            )