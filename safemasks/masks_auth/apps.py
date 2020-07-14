from django.apps import AppConfig


class MasksAuthConfig(AppConfig):
    name = "safemasks.masks_auth"

    def ready(self):
        import safemasks.masks_auth.signals
