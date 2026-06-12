
# ---------------------------
# CONTEXT MIXIN
# ---------------------------
class ContextMixin:
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
