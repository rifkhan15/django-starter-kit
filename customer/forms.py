from django.forms import inlineformset_factory
from .models import Inquiry, InquiryItem

InquiryFormSet = inlineformset_factory(
    Inquiry,
    InquiryItem,
    fields="__all__",
    extra=5,
    can_delete=True,
)