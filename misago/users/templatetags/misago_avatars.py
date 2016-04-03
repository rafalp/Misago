from django import template
from django.core.urlresolvers import reverse


register = template.Library()


@register.filter(name='avatar')
def avatar(user, size=200):
    return reverse('misago:user-avatar', kwargs={
        'pk': user.pk,
        'hash': user.avatar_hash,
        'size': size
    })


@register.simple_tag
def blankavatar(size=200):
    return reverse('misago:blank-avatar', kwargs={'size': size})
