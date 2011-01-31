# import socket
# from functools import wraps

from django import template
from django.conf import settings
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def shorten(value, arg = "10 ..."):
    args = arg.split()
    l = int(args[0])
    s = str(value)
    if len(s) > l:
        ss = str(args[1])
        return s[:l - len(ss)] + ss
    return s


# @register.filter
# def naturaldate(value, arg):
#     if not value:
#         return ''
#     if arg is None:
#         arg = settings.DATE_FORMAT
#     return HumanizedDateFormat(value).format(arg)
# 
# 
# @register.filter
# def name_or_username(user):
#     """Accepts a user (not very robust) and returns either their full name or their username."""
#     if not isinstance(user, User):
#         return False
#     return user.get_full_name() or user.username
# 
# 
# @register.filter
# def posessive(string):
#     if not string:
#         return ''
#     suffix = "%s's"
#     if string.lower()[-1] == 's':
#         suffix = "%s'"
#     
#     return suffix % (string)
# 
# 
# @register.filter
# def contains(value, arg):
#     return arg in value