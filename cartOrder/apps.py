from django.apps import AppConfig


class CartorderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cartOrder'

    # initialize the django-signals
    def ready(self):
        import cartOrder.signals