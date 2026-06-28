# defin the class names of the crud models and models that need navigation.
APP_CONFIG = {
    "crud_models": [
        "Customer",
        "Company",
        "Inquiry",
        "InquiryItem",
    ],
    "nav_excludes": [
        "InquiryItem",
    ]
}