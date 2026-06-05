from django.contrib import admin
from customer.models import Customer, Inquiry, InquiryItem

admin.site.register(Customer)
admin.site.register(Inquiry)
admin.site.register(InquiryItem)