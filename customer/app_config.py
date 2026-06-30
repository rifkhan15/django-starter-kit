from .models import Customer, Company, Inquiry, InquiryItem

APP_CONFIG = {
    "crud_models": [
        Customer,
        Company,
        Inquiry,
        InquiryItem,
    ],

    # models not shown in menu
    "nav_hidden": [
        InquiryItem,
    ],

    # list URL override
    "list_redirects": {
        InquiryItem: Inquiry,
    },
}