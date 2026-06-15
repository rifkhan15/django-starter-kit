from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from core.mixins import CommonLabelsMixin, ChildrenMixin, InlineFormsetLabelsMixin
from core.config_loader import load_app_configs

configs = load_app_configs()

# ---------------------------
# BASE VIEW
# ---------------------------
class BaseView(CommonLabelsMixin):

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
        paginate_by = 35

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
                f"{app_label}/create.html",
                "core/create.html",
            ]

        def get_success_url(self):
            model_name = self.model._meta.model_name

            if self.has_formset():
                return f"/{app_label}/{model_name}/{self.object.pk}/update/"

            return f"/{app_label}/{model_name}/"

    # ---------------- UPDATE VIEW ----------------
    class U(BaseView, InlineFormsetLabelsMixin, UpdateView):
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

            formset = self.get_inline_formset()

            if formset:
                ctx["formset"] = formset(
                    self.request.POST or None,
                    instance=self.object,
                )

            return ctx

        def form_valid(self, form):
            self.object = form.save()

            formset = self.get_inline_formset()

            if formset:
                fs = formset(self.request.POST, instance=self.object)

                if fs.is_valid():
                    fs.save()
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

    # ---------------- ATTACH ----------------
    for view in (L, D, C, U, X):
        view.model = model
        view.app_label = app_label

    return L, D, C, U, X