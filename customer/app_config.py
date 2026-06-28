# from .models import (
#     Customer,
#     Company,
#     Inquiry,
#     InquiryItem,
# )

# # defin the models that need crud system. define models that does not need navigation.
# APP_CONFIG = {
#     "crud_models" : [
#         Customer,
#         Company,
#         Inquiry,
#         InquiryItem,
#     ],
#     "nav_excludes" : [
#         {"exclude_model" : InquiryItem}, {"list_redirect_model" : Inquiry}, 
#     ],
# }

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