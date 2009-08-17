# This was taken from django-registration (mostly, anyway)

from django.dispatch import Signal


# A new user has registered.
user_registered = Signal(providing_args=["user"])
