# defin the models that need crud system and navigation.
# APP_CONFIG = {
#     "crud_models": [
#         "Customer",
#         "Company",
#         "Inquiry",
#         "InquiryItem",
#     ],
#     "nav_excludes": [
#         "InquiryItem",
#     ]
# }

from .models import (
    Customer,
    Company,
    Inquiry,
    InquiryItem,
)

APP_CONFIG = {
    "crud_models" : [
        Customer,
        Company,
        Inquiry,
        InquiryItem,
    ],
    "nav_excludes" : [
        InquiryItem,
    ],
}