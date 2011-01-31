"""Miscellaneous context processors."""
from django.conf import settings

def add_settings(request):
    """Adds a settings variable to the template context."""
    return { 'settings': settings }