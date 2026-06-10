from importlib import import_module

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from core.mixins import ContextMixin, ChildrenMixin
from core.config_loader import load_app_configs


configs = load_app_configs()


def get_formset_class(app_label, model_name):
    try:
        forms_module = import_module(f"{app_label}.forms")
        return getattr(forms_module, f"{model_name}FormSet", None)
    except (ModuleNotFoundError, AttributeError):
        return None


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

            if self.model_name == "Inquiry":
                return (
                    f"/{self.app_label.lower()}/"
                    f"{self.model_name.lower()}/"
                    f"{self.object.pk}/update/"
                )

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

            formset_class = get_formset_class(
                self.app_label,
                self.model_name,
            )

            if formset_class:
                if self.request.POST:
                    ctx["formset"] = formset_class(
                        self.request.POST,
                        instance=self.object,
                    )
                else:
                    ctx["formset"] = formset_class(
                        instance=self.object,
                    )

            ctx.update(self.get_common_context())
            return ctx

        def form_valid(self, form):

            formset_class = get_formset_class(
                self.app_label,
                self.model_name,
            )

            if not formset_class:
                return super().form_valid(form)

            self.object = form.save()

            formset = formset_class(
                self.request.POST,
                instance=self.object,
            )

            if formset.is_valid():
                formset.save()
                return super().form_valid(form)

            return self.render_to_response(
                self.get_context_data(form=form)
            )

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

    # ---------------- ATTACH CLASS ATTRIBUTES ----------------
    for view in (L, D, C, U, X):
        view.model = model
        view.app_label = app_label
        view.model_name = model_name

    return L, D, C, U, X