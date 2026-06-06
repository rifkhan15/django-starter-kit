from django.db import models

class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_date"]

    @property
    def field_attrs(self):
        return [
            (f.name, f.verbose_name.capitalize, getattr(self, f.name))
            for f in self._meta.fields
        ]
    
    @property
    def object_set_title(self):
        return self.object_set.model._meta.verbose_name_plural.title()