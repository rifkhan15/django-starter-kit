from django.db import models

class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        abstract = True

    @property
    def related_model_verbose_plural(self):
        return self.items.model._meta.verbose_name_plural

    @property
    def field_attrs(self):
        return [
            (f.name, f.verbose_name, getattr(self, f.name))
            for f in self._meta.fields
        ]
    