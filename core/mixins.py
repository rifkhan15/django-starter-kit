from importlib import import_module
from django.forms.models import BaseInlineFormSet

#name of common labels of models, urls, etc
class CommonLabelsMixin:
    def get_common_context(self):
        model = self.model
        model_name = model._meta.model_name

        return {
            "app_label": self.app_label,
            "model_name": model_name,
            "model_verbose_name": model._meta.verbose_name,
            "model_verbose_plural": model._meta.verbose_name_plural,
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

#child context for accessing children in detail template
# class RelatedObjectsMixin:
#     def get_related_data(self, obj):
#         related_data = []

#         for rel in obj._meta.related_objects:

#             accessor = rel.get_accessor_name()
#             manager = getattr(obj, accessor, None)

#             if manager is None:
#                 continue

#             related_data.append({
#                 "related_verbose_name_plural": rel.related_model._meta.verbose_name_plural,
#                 "items": manager.all(),
#             })

#         return related_data

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx["related_data"] = self.get_related_data(self.object)
#         return ctx

        
#inlineformset lables
class InlineFormsetLabelsMixin:
    def get_inline_formset(self):
        model = self.model

        try:
            forms_module = import_module(f"{self.app_label}.forms")
        except Exception:
            return None

        for obj in vars(forms_module).values():

            if (
                isinstance(obj, type)
                and issubclass(obj, BaseInlineFormSet)
                and getattr(obj, "fk", None)
                and obj.fk.remote_field.model == model
            ):
                return obj

        return None

    def get_formset_labels(self):
        formset = self.get_inline_formset()

        if not formset:
            return {"has_formset": False}

        child = formset.model

        return {
            "has_formset": True,
            "formset": formset,
            "formset_verbose_name": child._meta.verbose_name,
            "formset_verbose_name_plural": child._meta.verbose_name_plural,
        }

    def has_formset(self):
        return self.get_inline_formset() is not None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self.get_formset_labels())
        return ctx