import hashlib

from django import template


register = template.Library()


@register.filter(name='avatar')
def avatar(user, size=200):
    gravatar_hex = hashlib.md5(user.email).hexdigest()
    return '//www.gravatar.com/avatar/%s?s=%s' % (gravatar_hex, size)
