from django.apps import AppConfig


class coreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        from core.urls import generate_core_urls

        generate_core_urls()