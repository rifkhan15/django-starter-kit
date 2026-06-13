from importlib import import_module

from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from core.mixins import ChildrenMixin
from core.config_loader import load_app_configs


configs = load_app_configs()

def get_formset_class(app_label, model_name):
    try:
        forms_module = import_module(f"{app_label}.forms")
        return getattr(forms_module, f"{model_name}FormSet", None)
    except (ModuleNotFoundError, AttributeError):
        return None

class BaseView:
    def get_common_context(self):
            model = self.model

            model_name_lower = self.model_name.lower()

            return {
                "app_label": self.app_label,
                "model_name": self.model_name,
                "model_name_lower": model_name_lower,
                "model_verbose_name": model._meta.verbose_name,
                "model_title_plural": model._meta.verbose_name_plural.title(),

                "list_url": f"{self.app_label}_{model_name_lower}_list",
                "create_url": f"{self.app_label}_{model_name_lower}_create",
                "detail_url": f"{self.app_label}_{model_name_lower}_detail",
                "update_url": f"{self.app_label}_{model_name_lower}_update",
                "delete_url": f"{self.app_label}_{model_name_lower}_delete",
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

        search_fields = self.get_search_fields()

        if not search_fields:
            return queryset

        filters = Q()

        for field in search_fields:
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

    # ---------------- LIST VIEW ----------------
    class L(BaseView, ListView):
        paginate_by = 15

        def get_template_names(self):
            return [
                f"{self.app_label}/list.html",
                "core/list.html",
            ]

        def get_queryset(self):
            qs = super().get_queryset()
            return self.apply_search(qs)

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            ctx.update(self.get_search_context())
            return ctx

    # ---------------- DETAIL VIEW ----------------
    class D(BaseView, ChildrenMixin, DetailView):
        template_name = "core/detail.html"

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            ctx["children"] = self.get_children(self.object)
            return ctx

    # ---------------- CREATE VIEW ----------------
    class C(BaseView,  CreateView):
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

    # ---------------- UPDATE VIEW ----------------
    class U(BaseView, UpdateView):
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
    class X(BaseView, DeleteView):
        template_name = "core/confirm_delete.html"

        def get_success_url(self):
            return f"/{self.app_label.lower()}/{self.model_name.lower()}/"

    # ---------------- ATTACH CLASS ATTRIBUTES ----------------
    for view in (L, D, C, U, X):
        view.model = model
        view.app_label = app_label
        view.model_name = model_name

    return L, D, C, U, X