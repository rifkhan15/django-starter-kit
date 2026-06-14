from importlib import import_module

from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from core.mixins import ChildrenMixin, InlineFormsetLabelsMixin
from core.config_loader import load_app_configs

configs = load_app_configs()


# ---------------------------
# FORMSET LOADER
# ---------------------------
def get_formset_class(app_label, model_name):
    try:
        forms_module = import_module(f"{app_label}.forms")
        return getattr(forms_module, f"{model_name.title()}FormSet", None)
    except (ModuleNotFoundError, AttributeError):
        return None


# ---------------------------
# BASE VIEW
# ---------------------------
class BaseView:
    def get_common_context(self):
        model = self.model
        model_name = model._meta.model_name

        return {
            "app_label": self.app_label,
            "model_name": model_name,
            "model_verbose_name": model._meta.verbose_name,
            "model_title_plural": model._meta.verbose_name_plural.title(),

            "list_url": f"{self.app_label}_{model_name}_list",
            "create_url": f"{self.app_label}_{model_name}_create",
            "detail_url": f"{self.app_label}_{model_name}_detail",
            "update_url": f"{self.app_label}_{model_name}_update",
            "delete_url": f"{self.app_label}_{model_name}_delete",
        }

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self.get_common_context())
        return ctx

    def get_queryset(self):
        return self.model.objects.all()

    def get_search_fields(self):
        return getattr(self.model, "SEARCH_FIELDS", [])

    def apply_search(self, queryset):
        q = self.request.GET.get("q", "").strip()

        if not q:
            return queryset

        filters = Q()

        for field in self.get_search_fields():
            filters |= Q(**{f"{field}__icontains": q})

        return queryset.filter(filters)

    def get_search_context(self):
        return {
            "search_query": self.request.GET.get("q", ""),
        }


# ---------------------------
# VIEW FACTORY
# ---------------------------
def make_views(*, model, app_label, model_name):

    model_name = model._meta.model_name

    # ---------------- LIST VIEW ----------------
    class L(BaseView, ListView):
        paginate_by = 25

        def get_template_names(self):
            return [
                f"{app_label}/list.html",
                "core/list.html",
            ]

        def get_queryset(self):
            return self.apply_search(super().get_queryset())

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            ctx.update(self.get_search_context())
            return ctx

    # ---------------- DETAIL VIEW ----------------
    class D(BaseView, ChildrenMixin, DetailView):

        def get_template_names(self):
            return [
                f"{app_label}/detail.html",
                "core/detail.html",
            ]

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            ctx["children"] = self.get_children(self.object)
            return ctx

    # ---------------- CREATE VIEW ----------------
    class C(BaseView, InlineFormsetLabelsMixin, CreateView):
        fields = "__all__"

        def get_template_names(self):
            return [
                f"{self.app_label}/create.html",
                "core/create.html",
            ]

        def get_success_url(self):
            if self.has_formset():
                return f"/{app_label}/{model_name}/{self.object.pk}/update/"
            return f"/{app_label}/{model_name}/"

    # ---------------- UPDATE VIEW ----------------
    class U(BaseView,InlineFormsetLabelsMixin, UpdateView):
        fields = "__all__"

        def get_template_names(self):
            return [
                f"{app_label}/update.html",
                "core/update.html",
            ]

        def get_success_url(self):
            return f"/{app_label}/{model_name}/"

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)

            formset_class = get_formset_class(app_label, model_name)

            if formset_class:
                ctx["formset"] = formset_class(
                    self.request.POST or None,
                    instance=self.object,
                )

            return ctx

        def form_valid(self, form):
            formset_class = get_formset_class(app_label, model_name)

            self.object = form.save()

            if formset_class:
                formset = formset_class(self.request.POST, instance=self.object)

                if formset.is_valid():
                    formset.save()
                else:
                    return self.render_to_response(
                        self.get_context_data(form=form)
                    )

            return super().form_valid(form)

    # ---------------- DELETE VIEW ----------------
    class X(BaseView, DeleteView):

        def get_template_names(self):
            return [
                f"{app_label}/confirm_delete.html",
                "core/confirm_delete.html",
            ]

        def get_success_url(self):
            return f"/{app_label}/{model_name}/"

    # ---------------- ATTACH ATTRIBUTES ----------------
    for view in (L, D, C, U, X):
        view.model = model
        view.app_label = app_label

    return L, D, C, U, X