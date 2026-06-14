from django.forms.models import BaseInlineFormSet

#child context for accessing children in detail template
class ChildrenMixin:
    def get_children(self, obj):
        children = []

        for rel in obj._meta.related_objects:

            manager = getattr(
                obj,
                rel.get_accessor_name(),
                None,
            )

            if manager is None:
                continue

            children.append({
                "verbose_name": rel.related_model._meta.verbose_name,
                "verbose_name_plural": rel.related_model._meta.verbose_name_plural,
                "items": manager.all(),
            })

        return children
        
#inlineformset lables
class InlineFormsetLabelsMixin:
    def get_inline_formset(self):
        model = self.model

        try:
            from importlib import import_module
            forms_module = import_module(f"{self.app_label}.forms")
        except Exception:
            return None

        for obj in vars(forms_module).values():

            if (
                isinstance(obj, type)
                and issubclass(obj, BaseInlineFormSet)
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
            "formset_verbose_name": child._meta.verbose_name,
            "formset_verbose_name_plural": child._meta.verbose_name_plural,
        }

    def has_formset(self):
        return self.get_inline_formset() is not None
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self.get_formset_labels())
        return ctx