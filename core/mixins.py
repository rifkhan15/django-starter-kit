from customer.models import Contact
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

# ---------------------------
# EXTRA CONTENT MIXIN
# ---------------------------
class ListContextMixin:
    def get_contact_context(self):
        return {
            "contacts_no_company": Contact.objects.filter(
                company__isnull=True
            )
        }