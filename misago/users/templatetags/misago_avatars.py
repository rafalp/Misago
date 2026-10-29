from django import template

register = template.Library()


@register.filter(name="avatar")
def avatar(user, size=200):
    if isinstance(user, dict):
        avatars = user["avatars"]
    else:
        avatars = user.avatars

    found_avatar = avatars[0]
    for user_avatar in avatars:
        if user_avatar["size"] >= size:
            found_avatar = user_avatar
    return found_avatar["url"]
