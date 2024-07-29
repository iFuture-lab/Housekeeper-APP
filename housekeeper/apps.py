from django.apps import AppConfig


class HousekeeperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'housekeeper'
    def ready(self):
        import housekeeper.signals
    


    
