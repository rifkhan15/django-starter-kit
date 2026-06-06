from django.db import models
from crud.models import BaseModel

class Company(BaseModel):
    company_name = models.CharField(max_length=200, unique=True)
    company_type = models.CharField(max_length=250, blank=True, null=True)
    contact_number = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField()

    def __str__(self):
        return self.company_name
    
    class Meta:
        verbose_name_plural = 'Companies'

class Contact(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    contact_number = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, blank=True, null=True, related_name='contacts')
    designation = models.CharField(max_length=150, blank=True, null=True)
    
    def __str__(self):
        if self.company:
            return f"{self.name} - {self.company}"
        return self.name
    
class Inquiry(BaseModel):
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT, related_name='inquiries', verbose_name='Inquired by (contact name)')
    inquiry_date = models.DateField()
    
    @property
    def inquiry_number(self):
        return f"INQ-{self.pk:03d}"
        
    def __str__(self):
        return self.inquiry_number
    
    class Meta:
        verbose_name_plural = 'Inquiries'

class InquiryItem(BaseModel):
    inquiry_number = models.ForeignKey(Inquiry, on_delete=models.PROTECT, related_name='object_set')
    item_description = models.CharField(max_length=255) 
    special_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.item_description