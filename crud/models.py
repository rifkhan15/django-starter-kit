from django.db import models

class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_date"]