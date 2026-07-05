import django_filters

from .models import Inquiry

class InquiryFilter(django_filters.FilterSet):
    class Meta:
        model = Inquiry
        fields = ["status", "inquiry_number"]