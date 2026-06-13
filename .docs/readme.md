- webdesk is a django template to build core apps, and extinsible for non-core logic as well.
- it comes with these default apps: login, dashboard and core.
- core app works as a fully automatic views and urlpattern generator.
- once a new app is started, make an app_config.py file and define the app label, model names and extra_context as follows. 
        APP_CONFIG = {
            "model_names": ["Order", "Customer"]
        }
    - app_config is the main source for automatic creation of view and core navs. core navs are made in core/context_processors.py.
- default templates are in core/tempaltes/core. custom templates must be saved in same file name in app/templates/app_label. core/views will handle.
- defind inlineformset (children) in indivual forms.py (e.g. customer/forms.py)
- children add button is actually the parent's save button's success url set to update view
- user management must be prformed via django admin/ portal. the login app is a basic code for login, logout functionality.
- dashboard app can be coded accroding to business requirement.