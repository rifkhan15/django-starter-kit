from django.forms.models import BaseInlineFormSet

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