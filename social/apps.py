# social/apps.py
# AppConfig for the social app.
# The ready() method is called by Django when the app finishes loading.
# We use it to import signals.py so Django registers
# all the signal listeners when the server starts.
#
# Without this, signals.py would never be imported and
# notifications would never be created automatically.

from django.apps import AppConfig


class SocialConfig(AppConfig):
    """
    Configuration class for the social app.
    Django automatically uses this when 'social' is in INSTALLED_APPS.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social'

    def ready(self):
        """
        Called by Django once the app registry is fully populated.
        Importing signals here ensures all @receiver decorators
        are registered before any requests are processed.
        """
        import social.signals   # noqa — imported for side effects (registering signals)