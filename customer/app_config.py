from .models import Customer, Company, Inquiry, InquiryItem

APP_CONFIG = {
    "crud_models": [
        Customer,
        Company,
        Inquiry,
        InquiryItem,
    ],

    "nav_hidden": [
        InquiryItem,
    ],

    "list_redirects": {
        InquiryItem: Inquiry,
    },
}