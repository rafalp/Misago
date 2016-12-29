from django import template
from django.urls import reverse


register = template.Library()


@register.filter(name='avatar')
def avatar(user, size=200):
    found_avatar = user.avatars[0]
    for user_avatar in user.avatars:
        if user_avatar['size'] >= size:
            found_avatar = user_avatar
    return found_avatar['url']


@register.simple_tag
def blankavatar(size=200):
    return reverse('misago:blank-avatar', kwargs={'size': size})
