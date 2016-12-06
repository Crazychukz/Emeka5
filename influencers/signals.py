__author__ = 'CrazychukZ'

from django.dispatch import Signal


# A new user has registered.
user_registered = Signal(providing_args=["user", "request"])
