- webdesk 
  webdesk is a django template to build crud apps, and extinsible for non-crud logic as well.

- what's inside?
  default apps: login, dashboard and core.
  base templates are in webdesk/templates

- login
  user management must be prformed via django admin/ portal. 
  the login app is a basic design for login/logout functionality.

- dashboard
  dashboard app can be coded accroding to business requirement.

- core app 
  works as a fully automatic views and urlpattern generator.

- your new apps
  once a new app is started, make an app_config.py file and define the app label, model names and extra_context as follows. 
        APP_CONFIG = {
            "modelclass_names": ["Order", "Customer"]
        }
    *app_config is the main source for automatic creation of view and core navs. core navs are made in core/context_processors.py.

- templates
  default templates are in core/tempaltes/core. 
  any custom template must be saved in same file name in app/templates/app_label and core/views will handle automatically.

- children
  core/mixins.ChildrenMixin exposes child items with model labels. core/detail template has basic rendering.

- inlineformset
  if a formset is needed, define it inindivual forms.py (e.g. customer/forms.py)
  create success url of models with inlineformset set to udaate_url so after saving parent, the formset will render. 
