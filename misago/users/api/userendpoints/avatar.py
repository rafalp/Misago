import json

from django.core.exceptions import PermissionDenied, ValidationError
from django.utils.translation import ugettext as _

from rest_framework import status
from rest_framework.response import Response

from misago.conf import settings
from misago.core.utils import format_plaintext_for_html
from misago.users import avatars
from misago.users.forms.moderation import ModerateAvatarForm


def avatar_endpoint(request, pk=None):
    if request.user.is_avatar_locked:
        if request.user.avatar_lock_user_message:
            reason = format_plaintext_for_html(
                request.user.avatar_lock_user_message)
        else:
            reason = None

        return Response({
                'detail': _("Your avatar is locked. You can't change it."),
                'reason': reason
            },
            status=status.HTTP_403_FORBIDDEN)

    avatar_options = get_avatar_options(request.user)
    if request.method == 'POST':
        return avatar_post(avatar_options, request.user, request.data)
    else:
        return Response(avatar_options)


def get_avatar_options(user):
    options = {
        'avatar_hash': user.avatar_hash,

        'generated': True,
        'gravatar': False,
        'crop_org': False,
        'crop_tmp': False,
        'upload': False,
        'galleries': False
    }

    # Allow existing galleries
    if avatars.gallery.galleries_exist():
        options['galleries'] = avatars.gallery.get_available_galleries()

    # Can't have custom avatar?
    if not settings.allow_custom_avatars:
        return options

    # Allow Gravatar download
    options['gravatar'] = True

    # Get avatar tokens
    tokens = avatars.get_user_avatar_tokens(user)

    # Allow crop with token if we have uploaded avatar
    if avatars.uploaded.has_original_avatar(user):
        try:
            options['crop_org'] = {
                'secret': tokens['org'],
                'crop': json.loads(user.avatar_crop),
                'size': max(settings.MISAGO_AVATARS_SIZES)
            }
        except (TypeError, ValueError):
            pass

    # Allow crop of uploaded avatar
    if avatars.uploaded.has_temporary_avatar(user):
        options['crop_tmp'] = {
            'secret': tokens['tmp'],
            'size': max(settings.MISAGO_AVATARS_SIZES)
        }

    # Allow upload conditions
    options['upload'] = {
        'limit': settings.avatar_upload_limit * 1000,
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
            return Response({'detail': _("This avatar type is not allowed.")},
                            status=status.HTTP_400_BAD_REQUEST)

        rpc_handler = AVATAR_TYPES[data.get('avatar', 'nope')]
    except KeyError:
        return Response({'detail': _("Unknown avatar type.")},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        response_dict = {'detail': rpc_handler(user, data)}
    except AvatarError as e:
        return Response({'detail': e.args[0]},
                        status=status.HTTP_400_BAD_REQUEST)

    user.avatar_hash = avatars.get_avatar_hash(user)
    user.save(update_fields=['avatar_hash', 'avatar_crop'])
    response_dict['avatar_hash'] = user.avatar_hash

    response_dict['options'] = get_avatar_options(user)

    return Response(response_dict)


"""
Avatar rpc handlers
"""
def avatar_generate(user, data):
    avatars.dynamic.set_avatar(user)
    return _("New avatar based on your account was set.")


def avatar_gravatar(user, data):
    try:
        avatars.gravatar.set_avatar(user)
        return _("Gravatar was downloaded and set as new avatar.")
    except avatars.gravatar.GravatarError:
        raise AvatarError(_("Failed to connect to Gravatar servers."))
    except avatars.gravatar.NoGravatarAvailable:
        raise AvatarError(
            _("No Gravatar is associated with your e-mail address."))


def avatar_gallery(user, data):
    image = data.get('image') or 'not-possible'
    if avatars.gallery.is_avatar_from_gallery(image):
        avatars.gallery.set_avatar(user, image)
        return _("Avatar from gallery was set.")
    else:
        raise AvatarError(_("Incorrect image."))


def avatar_upload(user, data):
    new_avatar = data.get('image')
    if not new_avatar:
        raise AvatarError(_("No file was sent."))

    try:
        avatars.uploaded.handle_uploaded_file(user, new_avatar)
    except ValidationError as e:
        raise AvatarError(e.args[0])

    # send back token for temp image
    return avatars.get_avatar_hash(user, 'tmp')


def avatar_crop_org(user, data):
    avatar_crop(user, data, 'org')
    return _("Avatar was re-cropped.")


def avatar_crop_tmp(user, data):
    avatar_crop(user, data, 'tmp')
    return _("Uploaded avatar was set.")


def avatar_crop(user, data, suffix):
    try:
        crop = avatars.uploaded.crop_source_image(
            user, suffix, data.get('crop', {}))
        user.avatar_crop = json.dumps(crop)
    except ValidationError as e:
        raise AvatarError(e.args[0])


AVATAR_TYPES = {
    'generated': avatar_generate,
    'gravatar': avatar_gravatar,
    'galleries': avatar_gallery,
    'upload': avatar_upload,

    'crop_org': avatar_crop_org,
    'crop_tmp': avatar_crop_tmp,
}


def moderate_avatar_endpoint(request, profile):
    if request.method == "POST":
        is_avatar_locked = profile.is_avatar_locked
        form = ModerateAvatarForm(request.data, instance=profile)
        if form.is_valid():
            if form.cleaned_data['is_avatar_locked'] and not is_avatar_locked:
                avatars.dynamic.set_avatar(profile)
                profile.avatar_hash = avatars.get_avatar_hash(profile)
            form.save()

            return Response({
                'avatar_hash': profile.avatar_hash,
                'is_avatar_locked': int(profile.is_avatar_locked),
                'avatar_lock_user_message': profile.avatar_lock_user_message,
                'avatar_lock_staff_message': profile.avatar_lock_staff_message,
            })
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            'is_avatar_locked': int(profile.is_avatar_locked),
            'avatar_lock_user_message': profile.avatar_lock_user_message,
            'avatar_lock_staff_message': profile.avatar_lock_staff_message,
        })
