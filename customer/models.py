from django.db import models
from core.models import BaseModel

class Company(BaseModel):
    company_name = models.CharField(max_length=200, unique=True)
    company_type = models.CharField(max_length=250, blank=True, null=True)
    contact_number = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField()

    SEARCH_FIELDS = [
        'company_name',
    ]

    def __str__(self):
        return self.company_name
    
    class Meta:
        verbose_name_plural = 'Companies'

class Customer(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    contact_number = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, blank=True, null=True)
    designation = models.CharField(max_length=150, blank=True, null=True)
    
    SEARCH_FIELDS = [
        'name',
    ]

    def __str__(self):
        return  f"{self.name} - {self.company}" if self.company else self.name
    
class Inquiry(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name='Inquired by (customer name)')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True, editable=False)
    inquiry_date = models.DateField()

    def save(self, *args, **kwargs):
        self.company = self.customer.company
        super().save(*args, **kwargs)

    @property
    def inquiry_number(self):
        return f"INQ-{self.pk:03d}"
    
    SEARCH_FIELDS = [
        'company'
        'item_description',
    ]
    
    def __str__(self):
        return self.inquiry_number
    
    class Meta:
        verbose_name_plural = 'Inquiries'

class InquiryItem(BaseModel):
    inquiry_number = models.ForeignKey(Inquiry, on_delete=models.PROTECT)
    item_description = models.CharField(max_length=255) 
    special_notes = models.TextField(blank=True, null=True)

    SEARCH_FIELDS = [
        'item_description',
    ]

    def __str__(self):
        return self.item_description