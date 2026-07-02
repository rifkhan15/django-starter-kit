from django.db import models
from core.models import BaseModel

class Company(BaseModel):
    company_name = models.CharField(max_length=200, unique=True)
    company_type = models.CharField(max_length=250, blank=True, null=True)
    contact_number = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField()

    SEARCH_FIELDS = ['company_name',]

    def __str__(self):
        return self.company_name
    
    class Meta:
        verbose_name_plural = 'companies'
        ordering = ["id"]

Company._meta.get_field("company_name").is_link=True

class Customer(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    contact_number = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    designation = models.CharField(max_length=150, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, blank=True, null=True, related_name="items")
    
    SEARCH_FIELDS = ['name',]
    
    def __str__(self):
        return  f"{self.name} - {self.company}" if self.company else self.name

Customer._meta.get_field("name").is_link=True

class Inquiry(BaseModel):
    inquiry_number = models.CharField(max_length=10, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="items")
    inquiry_date = models.DateField()

    SEARCH_FIELDS = ['inquiry_number', 'items__item_description']
    PAGINATE_BY_RELATED = "items"

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)  # first insert → get PK

        if is_new and not self.inquiry_number:
            self.inquiry_number = f"Q-{self.pk:04d}"

            Inquiry.objects.filter(pk=self.pk).update(
                inquiry_number=self.inquiry_number
            )

    def __str__(self):
        return self.inquiry_number
    
    class Meta:
        verbose_name_plural = 'inquiries'
        ordering = ['-inquiry_date']

class InquiryItem(BaseModel):
    inquiry_number = models.ForeignKey(Inquiry, on_delete=models.PROTECT, related_name="items")
    item_description = models.CharField(max_length=255) 
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(choices=[("pending", "Pending"), ("completed", "Completed")], default="pending")

    SEARCH_FIELDS = ['item_description',]

    def __str__(self):
        return f"Item no: {self.id} : {self.item_description}"
