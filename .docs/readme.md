- webdesk 
  webdesk is a django template to build crud apps, and extinsible for non-crud logic as well.

- what's inside?
  default apps: login, dashboard and core.
  base templates are in webdesk/templates

- login
  user management to be prformed via django admin/ portal. 
  the login app is a basic design for login/logout functionality.

- dashboard
  dashboard app can be coded accroding to business requirement.

- core app 
  works as a fully automatic views and urlpattern generator. list view queryset is set up to access related objects (object_list > object > related_list).

- your new apps
  once a new app is started, make an app_config.py file and define the class names of crud model and models that need navigation. 
  app_config is the main source for automatic creation of view and core navs. core navs are made in core/context_processors.py.
 

       APP_CONFIG = {
          "crud_models": [
              "Customer",
              "Company",
              "Inquiry",
              "InquiryItem",
          ],
          "nav_excludes": [
              "Inquiry",
          ]
}
    
- children
  core/mixins.ChildrenMixin exposes child items with model labels. core/detail template has basic rendering.

- inlineformset
  if a formset is needed, define it inindivual forms.py (e.g. customer/forms.py)
  create success url of models with inlineformset set to update_url so after saving parent, the formset will render. 

- templates
  default templates are in core/tempaltes/core. 
  any custom template must be saved in app/templates/app_label/ and the file name should be e.g. {model_name}_list.html. core/views will handle automatically. e.g. inauiry_list.html in the sample app.

- navs
  nav items are dynamically generated using the contextprocessor.crud_menu(). if a model class need excluding from menu, defin it in app_config.py.

- dashboard
  dashboard must be fully custmized according to business apps. there is no automaric system.


# 🚀 Dynamic Django Business Application Framework

A lightweight, configuration-driven Django backend system for rapidly building internal business applications with minimal boilerplate.

## 📌 Overview

This project is a reusable backend framework designed to speed up the development of business systems such as:

- Customer management systems
- Inquiry / workflow tracking systems
- Admin dashboards
- Internal operational tools

It eliminates repetitive CRUD development by generating views, URLs, context data, and formset handling dynamically from configuration.

---

## ⚙️ Key Features

### 🔹 Dynamic CRUD Generation
Automatically generates:
- ListView
- DetailView
- CreateView
- UpdateView
- DeleteView

based on model configuration.

---

### 🔹 Inline Formset Support
- Automatic detection of inline formsets
- Context-aware formset injection
- Smart handling of parent-child relationships

---

### 🔹 Config-Driven Architecture
Define models in a simple config:

```python
APP_CONFIG = {
    "crud_models": [
        "Customer",
        "Company",
        "Inquiry",
        "InquiryItem",
    ]
}
```

The system automatically builds:
- Views
- URLs
- Menus
- Context variables

---

### 🔹 Automatic URL & Context System
No manual wiring required for:
- URL patterns
- Model-based navigation
- Template context variables

---

### 🔹 Smart Context Processors
Global menu and UI context generation for all apps.

---

## 🧠 Design Philosophy

- Reduce Django boilerplate
- Enable rapid business app development
- Centralize logic
- Keep configuration separate from implementation

---

## 🏗️ Tech Stack

- Python
- Django
- Class-Based Views
- Dynamic imports
- Meta-programming with Django apps/forms

---

## 📦 Use Cases

- CRM systems
- Internal business tools
- Workflow tracking systems
- Rapid MVP backends

---

## 🚀 Status

Prototype / evolving framework for production-style business systems.

---

## 👤 Author

Built by a Python/Django backend developer focused on business automation systems and scalable backend architecture.
