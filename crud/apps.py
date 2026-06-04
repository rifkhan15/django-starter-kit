from django.apps import AppConfig

class CrudConfig(AppConfig):
    name = "crud"

    def ready(self):
        from .autocrud import generate
        generate()
