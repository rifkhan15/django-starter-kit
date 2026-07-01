# Django Starter Kit (CRUD + UI)
  Reusable Django starter kit for building CRUD applications using Class-Based Views and server-side rendering via Django templates. Includes dynamic navigation, dashboard components, and a minimal built-in UI.

## Features
- Django authentication (login/logout via built-in auth. user creation via django admin)
- Auto-generated CRUD system for registered models
- Dynamic navigation based on model configuration
- Template-based UI (no frontend framework dependency)
- Inline formset handling for related objects
- Simple dashboard system (customizable per project)

## Project Structure

### Apps included
- authentication: login/logout flow using Django auth
- dashboard: custom dashboard layer
- core: dynamic CRUD engine and routing system

## Core System
The core app powers automatic CRUD generation, routing and crud templates.

### Features
- Auto-generates CRUD views from registered models
- Handles object relationships (parent → child models)
- Supports list, detail, update, and redirect flows

## App Configuration
Each app registers models through app_config.py.

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

### Options
- crud_models: models enabled for automatic CRUD generation  
- nav_hidden: models hidden from navigation  
- list_redirects: redirects child models to parent nav link (list view) 

## Forms & Inline Formsets
- Crud forms are defined in core
- Inline formsets are handled manually using Django inline formsets. Defined in app/forms.py
- Parent-child saving flows are managed through update_url

## Templates
- Uses Django template engine only
- custom templates can be defind as e.g. app_name/templates/app_name/{app_label}{model_name}_list.html. Core app auto-resolve templates using this pattern.

## Navigation System
- Navigation is generated dynamically
- Built from crud_models in app_config.py
- Hidden models are filtered via nav_hidden

## Dashboard
- Fully custom implementation
- No automatic logic included
- Designed per business requirement

## Purpose
This starter kit is designed for building:

- CRM systems  
- Order management systems  
- Sales tracking tools  
- Internal business applications  
- Custom CRUD admin panels  
- And, similar operations systems

## Notes
- Lightweight and template-driven
- No frontend framework required
- Designed for rapid backend-heavy development