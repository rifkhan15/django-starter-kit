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
        attrs = []

        for f in self._meta.fields:
            if isinstance(f, models.TextField):
                continue

            value = getattr(self, f.name)

            attrs.append(
                (
                    f.name,
                    f.verbose_name,
                    value,
                    f.primary_key,
                    (
                        f"{value._meta.app_label}{value._meta.model_name}_detail"
                        if f.is_relation and value
                        else None
                    ),
                )
            )

        return attrs