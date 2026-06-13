
# ---------------------------
# CONTEXT MIXIN
# ---------------------------

class TemplateMixin:
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["core_form"] = "core/partials/_form.html"
        ctx["app_form"] = f"{self.app_label.lower()}/partials/_form.html"
        return ctx

# ---------------------------
# CHILDREN MIXIN
# ---------------------------
class ChildrenMixin:
    def get_children(self, obj):
        children = []

        for rel in obj._meta.related_objects:
            accessor = rel.get_accessor_name()

            if not accessor:
                continue

            manager = getattr(obj, accessor, None)

            if manager is None:
                continue

            children.append({
                "related_name": accessor,
                "verbose_name": rel.related_model._meta.verbose_name,
                "verbose_name_plural": rel.related_model._meta.verbose_name_plural,
                "items": manager.all(),
            })

        return children
