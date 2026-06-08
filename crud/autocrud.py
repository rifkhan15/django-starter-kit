from importlib import import_module
from django.apps import apps
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from crud.mixins import ContextMixin, ChildrenMixin
from crud.config_loader import load_app_configs


configs =  load_app_configs()

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