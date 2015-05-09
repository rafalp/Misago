from django import template
from django.core.urlresolvers import reverse


register = template.Library()


@register.filter(name='avatar')
def avatar(user, size=200):
    return reverse('misago:user_avatar', kwargs={
        'user_id': user.id,
        'hash': user.avatar_hash,
        'size': size
    })


@register.simple_tag
def blankavatar(size=200):
    return reverse('misago:blank_avatar', kwargs={'size': size})
