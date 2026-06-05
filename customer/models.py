from django.db import models
from crud.models import BaseModel

class Customer(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    contact_numner = models.CharField(max_length=30)
    email = models.EmailField()
    company = models.CharField(max_length=200)
    designation = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name
    
class Inquiry(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    inquiry_date = models.DateField()
    
    @property
    def inquiry_number(self):
        return f"INQ-{self.pk}"
        
    def __str__(self):
        return self.inquiry_number

class InquiryItem(BaseModel):
    inquiry_number = models.ForeignKey(Inquiry, on_delete=models.PROTECT)
    item_description = models.CharField(max_length=255) 
    special_notes = models.TextField()

    def __str__(self):
        return self.item_description