from django.contrib import admin
from customer.models import Customer, Company, Inquiry, InquiryItem

admin.site.register(Customer)
admin.site.register(Company)
admin.site.register(Inquiry)
admin.site.register(InquiryItem)