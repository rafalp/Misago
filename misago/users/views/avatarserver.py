import os

from path import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_control, never_cache

from misago.core.fileserver import make_file_response

from misago.users.avatars import store


@cache_control(private=True, must_revalidate=True, max_age=5 * 24 * 3600)
def serve_blank_avatar(request, size):
    size = clean_size(size)
    avatar_dir = store.get_avatars_dir_path()
    avatar_file = get_blank_avatar_file(size)
    avatar_path = os.path.join(avatar_dir, avatar_file)
    return make_file_response(avatar_path, 'image/png')


@cache_control(private=True, must_revalidate=False)
def serve_user_avatar(request, pk, hash, size):
    size = clean_size(size)

    if int(pk) > 0:
        avatar_dir = store.get_avatars_dir_path(pk)
        avatar_file = get_user_avatar_file(pk, size)
        avatar_path = os.path.join(avatar_dir, avatar_file)

        if Path(avatar_path).exists():
            avatar_path = os.path.join(avatar_dir, avatar_file)
            return make_file_response(avatar_path, 'image/png')
        else:
            return serve_blank_avatar(request, size)
    else:
        return serve_blank_avatar(request, size)


@never_cache
def serve_user_avatar_source(request, pk, secret, hash):
    fallback_avatar = get_blank_avatar_file(min(settings.MISAGO_AVATARS_SIZES))
    User = get_user_model()

    if pk > 0:
        try:
            user = User.objects.get(pk=pk)

            tokens = store.get_user_avatar_tokens(user)
            suffix = tokens.get(secret)
            if suffix:
                avatar_file = get_user_avatar_file(user.pk, suffix)
            else:
                avatar_file = fallback_avatar
        except User.DoesNotExist:
            avatar_file = fallback_avatar
    else:
        avatar_file = fallback_avatar

    if avatar_file == fallback_avatar:
        avatar_dir = store.get_avatars_dir_path()
    else:
        avatar_dir = store.get_avatars_dir_path(pk)

    avatar_path = os.path.join(avatar_dir, avatar_file)
    return make_file_response(avatar_path, 'image/png')


def clean_size(size):
    size = int(size)
    if size not in settings.MISAGO_AVATARS_SIZES:
        found_size = max(settings.MISAGO_AVATARS_SIZES)
        for valid_size in sorted(settings.MISAGO_AVATARS_SIZES, reverse=True):
            if valid_size > size:
                found_size = valid_size
        return found_size
    return size


def get_user_avatar_file(pk, size):
    return '%s_%s.png' % (pk, size)


def get_blank_avatar_file(size):
    return '%s.png' % size
