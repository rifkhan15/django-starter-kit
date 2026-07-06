from core.filters import BaseFilterSet
from .models import InquiryItem

class InquiryItemFilter(BaseFilterSet):
    class Meta:
        model = InquiryItem
        fields = ['inquiry_number', 'status']