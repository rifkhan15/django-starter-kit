- webdesk is a django template to build crud apps, and extinsibla for non-crud business logic.
- it comes with these default apps: login, dashboard and crud.
- crud app works as a fully automatic crud app and urlpattern generator.
- once a new business app is started, make an app_config.py file and define the app name, model names and extra_context as follows. 
        APP_CONFIG = {
            "model_names": ["Order", "Customer"]
        }
    - app_config is the main source for automatic creation of view and crud navs. crud navs are made in crud/context_processors.py.
- user management must be prformed via django admin/ portal. the login app is a basic code for login, logout functionality.
- dashboard app can be coded accroding to business requirement.