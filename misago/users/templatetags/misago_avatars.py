import hashlib

from django import template
from django.core.urlresolvers import reverse


register = template.Library()


@register.filter(name='avatar')
def avatar(user, size=200):
    try:
        user_pk = user.pk
    except:
        user_pk = user

    return reverse('misago:user_avatar',
                   kwargs={'user_id': user_pk, 'size': size})


@register.simple_tag
def blankavatar(size=200):
    return reverse('misago:blank_avatar', kwargs={'size': size})
