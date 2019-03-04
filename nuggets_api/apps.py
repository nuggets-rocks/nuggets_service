from django.apps import AppConfig


class NuggetsApiConfig(AppConfig):
    name = 'nuggets_api'

    def ready(self):
        from . import signals
