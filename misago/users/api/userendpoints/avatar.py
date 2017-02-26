import json

from rest_framework import status
from rest_framework.response import Response

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from misago.conf import settings
from misago.core.utils import format_plaintext_for_html
from misago.users import avatars
from misago.users.models import AvatarGallery
from misago.users.serializers import ModerateAvatarSerializer


def avatar_endpoint(request, pk=None):
    if request.user.is_avatar_locked:
        if request.user.avatar_lock_user_message:
            reason = format_plaintext_for_html(request.user.avatar_lock_user_message)
        else:
            reason = None

        return Response(
            {
                'detail': _("Your avatar is locked. You can't change it."),
                'reason': reason,
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    avatar_options = get_avatar_options(request.user)
    if request.method == 'POST':
        return avatar_post(avatar_options, request.user, request.data)
    else:
        return Response(avatar_options)


def get_avatar_options(user):
    options = {
        'avatars': user.avatars,
        'generated': True,
        'gravatar': False,
        'crop_src': False,
        'crop_tmp': False,
        'upload': False,
        'galleries': False,
    }

    # Allow existing galleries
    if avatars.gallery.galleries_exist():
        options['galleries'] = []
        for gallery in avatars.gallery.get_available_galleries():
            gallery_images = []
            for image in gallery['images']:
                gallery_images.append({
                    'id': image.id,
                    'url': image.url,
                })
            options['galleries'].append({
                'name': gallery['name'],
                'images': gallery_images,
            })

    # Can't have custom avatar?
    if not settings.allow_custom_avatars:
        return options

    # Allow Gravatar download
    options['gravatar'] = True

    # Allow crop if we have uploaded temporary avatar
    if avatars.uploaded.has_source_avatar(user):
        try:
            options['crop_src'] = {
                'url': user.avatar_src.url,
                'crop': json.loads(user.avatar_crop),
                'size': max(settings.MISAGO_AVATARS_SIZES),
            }
        except (TypeError, ValueError):
            pass

    # Allow crop of uploaded avatar
    if avatars.uploaded.has_temporary_avatar(user):
        options['crop_tmp'] = {
            'url': user.avatar_tmp.url,
            'size': max(settings.MISAGO_AVATARS_SIZES),
        }

    # Allow upload conditions
    options['upload'] = {
        'limit': settings.avatar_upload_limit * 1024,
        'allowed_extensions': avatars.uploaded.ALLOWED_EXTENSIONS,
        'allowed_mime_types': avatars.uploaded.ALLOWED_MIME_TYPES,
    }

    return options


class AvatarError(Exception):
    pass


def avatar_post(options, user, data):
    try:
        type_options = options[data.get('avatar', 'nope')]
        if not type_options:
            return Response(
                {
                    'detail': _("This avatar type is not allowed."),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        rpc_handler = AVATAR_TYPES[data.get('avatar', 'nope')]
    except KeyError:
        return Response(
            {
                'detail': _("Unknown avatar type."),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        response_dict = {'detail': rpc_handler(user, data)}
    except AvatarError as e:
        return Response(
            {
                'detail': e.args[0],
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.save()

    response_dict.update(get_avatar_options(user))
    return Response(response_dict)


def avatar_generate(user, data):
    avatars.dynamic.set_avatar(user)
    return _("New avatar based on your account was set.")


def avatar_gravatar(user, data):
    try:
        avatars.gravatar.set_avatar(user)
        return _("Gravatar was downloaded and set as new avatar.")
    except avatars.gravatar.NoGravatarAvailable:
        raise AvatarError(_("No Gravatar is associated with your e-mail address."))
    except avatars.gravatar.GravatarError:
        raise AvatarError(_("Failed to connect to Gravatar servers."))


def avatar_gallery(user, data):
    try:
        image_pk = int(data.get('image'))
        image = AvatarGallery.objects.get(pk=image_pk)
        if image.gallery == '__default__':
            raise ValueError()
        avatars.gallery.set_avatar(user, image)
        return _("Avatar from gallery was set.")
    except (TypeError, ValueError, AvatarGallery.DoesNotExist):
        raise AvatarError(_("Incorrect image."))


def avatar_upload(user, data):
    new_avatar = data.get('image')
    if not new_avatar:
        raise AvatarError(_("No file was sent."))

    try:
        avatars.uploaded.handle_uploaded_file(user, new_avatar)
    except ValidationError as e:
        raise AvatarError(e.args[0])

    # send back url for temp image
    return user.avatar_tmp.url


def avatar_crop_src(user, data):
    avatar_crop(user, data, 'src')
    return _("Avatar was re-cropped.")


def avatar_crop_tmp(user, data):
    avatar_crop(user, data, 'tmp')
    return _("Uploaded avatar was set.")


def avatar_crop(user, data, suffix):
    try:
        crop = avatars.uploaded.crop_source_image(user, suffix, data.get('crop', {}))
        user.avatar_crop = json.dumps(crop)
    except ValidationError as e:
        raise AvatarError(e.args[0])


AVATAR_TYPES = {
    'generated': avatar_generate,
    'gravatar': avatar_gravatar,
    'galleries': avatar_gallery,
    'upload': avatar_upload,
    'crop_src': avatar_crop_src,
    'crop_tmp': avatar_crop_tmp,
}


def moderate_avatar_endpoint(request, profile):
    if request.method == "POST":
        is_avatar_locked = profile.is_avatar_locked
        serializer = ModerateAvatarSerializer(profile, data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['is_avatar_locked'] and not is_avatar_locked:
                avatars.dynamic.set_avatar(profile)
            serializer.save()

            return Response({
                'avatars': profile.avatars,
                'is_avatar_locked': int(profile.is_avatar_locked),
                'avatar_lock_user_message': profile.avatar_lock_user_message,
                'avatar_lock_staff_message': profile.avatar_lock_staff_message,
            })
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response({
            'is_avatar_locked': int(profile.is_avatar_locked),
            'avatar_lock_user_message': profile.avatar_lock_user_message,
            'avatar_lock_staff_message': profile.avatar_lock_staff_message,
        })
