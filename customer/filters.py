import django_filters

from .models import InquiryItem

class InquiryItemFilter(django_filters.FilterSet):
    class Meta:
        model = InquiryItem
        fields = ["status", "inquiry_number"]