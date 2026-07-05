from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from core.mixins import (
    CommonLabelsMixin,
    InlineFormsetLabelsMixin,
)

from django.core.paginator import Paginator
from django.core.paginator import Page
from importlib import import_module

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
            filters |= Q(
                **{
                    f"{field}__icontains": q
                }
            )

        return queryset.filter(filters).distinct()

    def get_search_context(self):
        return {
            "search_query": self.request.GET.get("q", ""),
        }


# ---------------------------
# VIEW FACTORY
# ---------------------------
def make_views(*, model):

    app_label = model._meta.app_label
    model_name = model._meta.model_name

    # Find FilterSet once
    try:
        module = import_module(f"{app_label}.filters")
        filterset_class = getattr(module, f"{model.__name__}Filter", None)
    except ModuleNotFoundError:
        filterset_class = None

    # ---------------- LIST ----------------
    class L(BaseView, ListView):
        paginate_by = 25

        def get_template_names(self):
            return [
                f"{app_label}/{model_name}_list.html",
                "core/list.html",
            ]

        def get_queryset(self):
            qs = super().get_queryset()

            related = [
                rel.get_accessor_name()
                for rel in self.model._meta.related_objects
                if rel.one_to_many or rel.many_to_many
            ]

            qs = self.apply_search(qs.prefetch_related(*related))

            if filterset_class:
                self.filterset = filterset_class(
                    self.request.GET,
                    queryset=qs,
                )
                qs = self.filterset.qs

            return qs

        def paginate_queryset(self, queryset, page_size):
            return super().paginate_queryset(queryset, page_size)

            page_number = int(self.request.GET.get(self.page_kwarg, 1))

            visible = []
            rows = 0

            start = (page_number - 1) * page_size
            end = page_number * page_size
            total = 0

            for obj in queryset:
                count = getattr(obj, related).count()
                count = max(count, 1)

                if (total < end and total + count > start):
                    visible.append(obj)

                total += count

            paginator = Paginator(range(total), page_size)

            page = Page(visible, page_number, paginator)

            return (paginator, page, visible, page.has_other_pages())

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            ctx.update(self.get_search_context())
            
            if filterset_class:
                ctx["filter"] = self.filterset
            
            return ctx

    # ---------------- DETAIL ----------------
    class D(BaseView, DetailView):

        def get_template_names(self):
            return [
                f"{app_label}/{model_name}_detail.html",
                "core/detail.html",
            ]

    # ---------------- CREATE ----------------
    class C(BaseView, InlineFormsetLabelsMixin, CreateView):
        fields = "__all__"

        def get_template_names(self):
            return [
                f"{app_label}/{model_name}_create.html",
                "core/create.html",
            ]

        def get_success_url(self):

            if self.has_formset():
                return (
                    f"/{app_label}/"
                    f"{model_name}/"
                    f"{self.object.pk}/update/"
                )

            return f"/{app_label}/{model_name}/"

    # ---------------- UPDATE ----------------
    class U(BaseView, InlineFormsetLabelsMixin, UpdateView):
        fields = "__all__"

        def get_template_names(self):
            return [
                f"{app_label}/{model_name}_update.html",
                "core/update.html",
            ]

        def get_success_url(self):
            return (
                f"/{app_label}/"
                f"{model_name}/"
                f"{self.object.pk}/"
            )

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
                fs = formset(
                    self.request.POST,
                    instance=self.object,
                )

                if fs.is_valid():
                    fs.save()
                else:
                    return self.render_to_response(
                        self.get_context_data(form=form)
                    )

            return super().form_valid(form)

    # ---------------- DELETE ----------------
    class X(BaseView, DeleteView):

        def get_template_names(self):
            return [
                f"{app_label}/{model_name}_confirm_delete.html",
                "core/confirm_delete.html",
            ]

        def get_success_url(self):
            return f"/{app_label}/{model_name}/"

    # ---------------- ATTACH ----------------
    for view in (L, D, C, U, X):
        view.model = model

    return L, D, C, U, X