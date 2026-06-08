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
from crud.mixins import ContextMixin, ChildrenMixin


crud_urlpatterns = []

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

# ---------------------------
# VIEW FACTORY
# ---------------------------
def make_views(*, model, app_label, model_name):

    # ---------------- LIST VIEW ----------------
    class L(ContextMixin, ListView):
        template_name = "list.html"

        def get_queryset(self):
            return model.objects.all()

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            ctx.update(self.get_common_context())
            return ctx

    # ---------------- DETAIL VIEW ----------------
    class D(ChildrenMixin, ContextMixin, DetailView):
        template_name = "detail.html"

        def get_queryset(self):
            return model.objects.all()

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            ctx.update(self.get_common_context())
            ctx["children"] = self.get_children(self.object)
            return ctx

    # ---------------- CREATE VIEW ----------------
    class C(ContextMixin, CreateView):
        template_name = "create.html"
        fields = "__all__"

        def get_queryset(self):
            return model.objects.all()

        def get_success_url(self):
            return f"/{self.app_label.lower()}/{self.model_name.lower()}/"

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            ctx.update(self.get_common_context())
            return ctx

    # ---------------- UPDATE VIEW ----------------
    class U(ContextMixin, UpdateView):
        template_name = "update.html"
        fields = "__all__"

        def get_queryset(self):
            return model.objects.all()

        def get_success_url(self):
            return f"/{self.app_label.lower()}/{self.model_name.lower()}/"

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            ctx.update(self.get_common_context())
            return ctx

    # ---------------- DELETE VIEW ----------------
    class X(ContextMixin, DeleteView):
        template_name = "confirm_delete.html"

        def get_queryset(self):
            return model.objects.all()

        def get_success_url(self):
            return f"/{self.app_label.lower()}/{self.model_name.lower()}/"

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            ctx.update(self.get_common_context())
            return ctx

    # ---------------- ATTACH CLASS ATTRIBUTES (IMPORTANT FIX) ----------------
    for view in (L, D, C, U, X):
        view.model = model
        view.app_label = app_label
        view.model_name = model_name

    return L, D, C, U, X


# ---------------------------
# URL GENERATION
# ---------------------------
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

            crud_urlpatterns += [
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