from django.apps import AppConfig


class AUserauthappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'a_userauthapp'

    def ready(self):
        import a_userauthapp.signals

