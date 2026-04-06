# apps.py
from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'users'

    # The ready() method runs as soon as Django starts your app
    def ready(self):
        # We import the signals here so Django starts listening for the events
        import users.signals