from django.contrib.auth import get_user_model
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import redirect

from misago.conf import settings


UserModel = get_user_model()


def user_avatar(request, pk, size):
    size = int(size)

    try:
        user = UserModel.objects.get(pk=pk)
    except UserModel.DoesNotExist:
        return blank_avatar(request)

    found_avatar = user.avatars[0]
    for avatar in user.avatars:
        if avatar['size'] >= size:
            found_avatar = avatar
    return redirect(found_avatar['url'])


def blank_avatar(request):
    return redirect(static(settings.MISAGO_BLANK_AVATAR))
