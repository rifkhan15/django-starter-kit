from importlib import import_module

from django.db.models import Q
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
# BASE VIEW
# ---------------------------
class BaseView:
    paginate_by = 25

    def get_queryset(self):
        return self.model.objects.all()

    def get_search_fields(self):
        return getattr(self.model, "SEARCH_FIELDS", [])

    def apply_search(self, queryset):

        q = self.request.GET.get("q", "").strip()

        if not q:
            return queryset

        search_fields = self.get_search_fields()

        if not search_fields:
            return queryset

        filters = Q()

        for field in search_fields:
            filters |= Q(**{f"{field}__icontains": q})

        return queryset.filter(filters)

    def get_common_context_data(self):
        return {
            "search_query": self.request.GET.get("q", ""),
        }


# ---------------------------
# VIEW FACTORY
# ---------------------------
def make_views(*, model, app_label, model_name):

    # ---------------- LIST VIEW ----------------
    class L(BaseView, ContextMixin, ListView):
        template_name = "core/list.html"

        def get_queryset(self):
            qs = super().get_queryset()
            return self.apply_search(qs)

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            ctx.update(self.get_common_context())
            ctx.update(self.get_common_context_data())
            return ctx

    # ---------------- DETAIL VIEW ----------------
    class D(BaseView, ChildrenMixin, ContextMixin, DetailView):
        template_name = "core/detail.html"

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            ctx.update(self.get_common_context())
            ctx["children"] = self.get_children(self.object)
            return ctx

    # ---------------- CREATE VIEW ----------------
    class C(BaseView, ContextMixin, CreateView):
        template_name = "core/create.html"
        fields = "__all__"

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
            ctx["core_form"] = "core/partials/_core_form.html"
            ctx["app_form"] = f"{self.app_label.lower()}/_app_form.html"
            return ctx

    # ---------------- UPDATE VIEW ----------------
    class U(BaseView, ContextMixin, UpdateView):
        template_name = "core/update.html"
        fields = "__all__"

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
    class X(BaseView, ContextMixin, DeleteView):
        template_name = "core/confirm_delete.html"

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