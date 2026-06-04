from django.db import models
from crud.models import BaseModel

class Customer(BaseModel):
    company = models.CharField(max_length=150, unique=True)
    
    def __str__(self):
        return self.company
    
class Brand(BaseModel):
    brand = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.brand