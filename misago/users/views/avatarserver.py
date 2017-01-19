from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import redirect


def user_avatar(request, pk, size):
    User = get_user_model()
    size = int(size)

    try:
        user = User.objects.get(pk=pk)

        found_avatar = user.avatars[0]
        for avatar in user.avatars:
            if avatar['size'] >= size:
                found_avatar = avatar
        return redirect(found_avatar['url'])
    except User.DoesNotExist:
        return blank_avatar(request)


def blank_avatar(request):
    return redirect(static(settings.MISAGO_BLANK_AVATAR))
