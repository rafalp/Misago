from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.templatetags.static import static

from ...conf import settings

User = get_user_model()


def user_avatar(request, pk, size):
    size = int(size)

    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return blank_avatar(request)

    found_avatar = user.avatars[0]
    for avatar in user.avatars:
        if avatar["size"] >= size:
            found_avatar = avatar
    return redirect(found_avatar["url"])


def blank_avatar(request):
    return redirect(
        request.settings.blank_avatar or static(settings.MISAGO_BLANK_AVATAR)
    )
