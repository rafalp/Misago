from path import Path
from PIL import Image

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from misago.conf import settings

from . import store


ALLOWED_EXTENSIONS = ('.gif', '.png', '.jpg', '.jpeg')
ALLOWED_MIME_TYPES = ('image/gif', 'image/jpeg', 'image/png', 'image/mpo')


def validate_file_size(uploaded_file):
    upload_limit = settings.avatar_upload_limit * 1024
    if uploaded_file.size > upload_limit:
        raise ValidationError(_("Uploaded file is too big."))


def validate_extension(uploaded_file):
    lowercased_name = uploaded_file.name.lower()
    for extension in ALLOWED_EXTENSIONS:
        if lowercased_name.endswith(extension):
            return True
    else:
        raise ValidationError(_("Uploaded file type is not allowed."))


def validate_mime(uploaded_file):
    if uploaded_file.content_type not in ALLOWED_MIME_TYPES:
        raise ValidationError(_("Uploaded file type is not allowed."))


def validate_dimensions(uploaded_file):
    image = Image.open(uploaded_file)

    min_size = max(settings.MISAGO_AVATARS_SIZES)
    if min(image.size) < min_size:
        message = _("Uploaded image should be at least %(size)s pixels tall and wide.")
        raise ValidationError(message % {'size': min_size})

    if image.size[0] * image.size[1] > 2000 * 3000:
        message = _("Uploaded image is too big.")
        raise ValidationError(message)

    image_ratio = float(min(image.size)) / float(max(image.size))
    if image_ratio < 0.25:
        message = _("Uploaded image ratio cannot be greater than 16:9.")
        raise ValidationError(message)
    return image


def validate_uploaded_file(uploaded_file):
    try:
        validate_file_size(uploaded_file)
        validate_extension(uploaded_file)
        validate_mime(uploaded_file)
        return validate_dimensions(uploaded_file)
    except ValidationError as e:
        try:
            temporary_file_path = Path(uploaded_file.temporary_file_path())
            if temporary_file_path.exists():
                temporary_file_path.remove()
        except Exception:
            pass
        raise e


def handle_uploaded_file(user, uploaded_file):
    image = validate_uploaded_file(uploaded_file)
    store.store_temporary_avatar(user, image)


def clean_crop(image, crop):
    message = _("Crop data is invalid. Please try again.")

    crop_dict = {}
    try:
        crop_dict = {
            'x': float(crop['offset']['x']),
            'y': float(crop['offset']['y']),
            'zoom': float(crop['zoom']),
        }
    except (KeyError, TypeError, ValueError):
        raise ValidationError(message)

    if crop_dict['zoom'] < 0 or crop_dict['zoom'] > 1:
        raise ValidationError(message)

    min_size = max(settings.MISAGO_AVATARS_SIZES)

    zoomed_size = (
        round(float(image.size[0]) * crop_dict['zoom'], 2),
        round(float(image.size[1]) * crop_dict['zoom'], 2)
    )

    if min(zoomed_size) < min_size:
        raise ValidationError(message)

    crop_square = {
        'x': crop_dict['x'] * -1,
        'y': crop_dict['y'] * -1,
    }

    if crop_square['x'] < 0 or crop_square['y'] < 0:
        raise ValidationError(message)

    if crop_square['x'] + min_size > zoomed_size[0]:
        raise ValidationError(message)

    if crop_square['y'] + min_size > zoomed_size[1]:
        raise ValidationError(message)

    return crop_dict


def crop_source_image(user, source, crop):
    if source == 'tmp':
        image = Image.open(user.avatar_tmp)
    else:
        image = Image.open(user.avatar_src)
    crop = clean_crop(image, crop)

    min_size = max(settings.MISAGO_AVATARS_SIZES)
    if image.size[0] == min_size and image.size[0] == image.size[1]:
        cropped_image = image
    else:
        upscale = 1.0 / crop['zoom']
        cropped_image = image.crop((
            int(round(crop['x'] * upscale * -1, 0)), int(round(crop['y'] * upscale * -1, 0)),
            int(round((crop['x'] - min_size) * upscale * -1, 0)),
            int(round((crop['y'] - min_size) * upscale * -1, 0)),
        ))

    store.store_avatar(user, cropped_image)
    if source == 'tmp':
        store.store_original_avatar(user)

    return crop


def has_temporary_avatar(user):
    return bool(user.avatar_tmp)


def has_source_avatar(user):
    return bool(user.avatar_src)
