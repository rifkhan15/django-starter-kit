from django.contrib import admin
from customer.models import Company, Contact, Inquiry, InquiryItem

admin.site.register(Company)
admin.site.register(Contact)
admin.site.register(Inquiry)
admin.site.register(InquiryItem)