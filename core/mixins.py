from importlib import import_module
from django.forms.models import BaseInlineFormSet

#name of common labels of models, urls, etc
class CommonLabelsMixin:

    def get_common_lables(self):
        model = self.model
        app_label = model._meta.app_label
        model_name = model._meta.model_name

        return {
            "app_label": app_label,
            "model_name": model_name,
            "model_verbose_name": model._meta.verbose_name,
            "model_verbose_plural": model._meta.verbose_name_plural,
            "model_title_plural": model._meta.verbose_name_plural.title(),

            "list_url": f"{app_label}{model_name}_list",
            "create_url": f"{app_label}{model_name}_create",
            "detail_url": f"{app_label}{model_name}_detail",
            "update_url": f"{app_label}{model_name}_update",
            "delete_url": f"{app_label}{model_name}_delete",
        }

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self.get_common_lables())
        return ctx
        
#inlineformset lables
class InlineFormsetLabelsMixin:
    def get_inline_formset(self):
        model = self.model

        app_label = model._meta.app_label

        try:
            forms_module = import_module(f"{app_label}.forms")
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

        rel_item = formset.model

        return {
            "has_formset": True,
            "formset": formset,
            "formset_verbose_name": rel_item._meta.verbose_name,
            "formset_verbose_name_plural": rel_item._meta.verbose_name_plural,
        }

    def has_formset(self):
        return self.get_inline_formset() is not None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self.get_formset_labels())
        return ctx