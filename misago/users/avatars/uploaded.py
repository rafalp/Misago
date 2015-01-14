from hashlib import sha256

from path import Path
from PIL import Image

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from misago.conf import settings

from misago.users.avatars import store


ALLOWED_EXTENSIONS = ('.gif', '.png', '.jpg', '.jpeg')
ALLOWED_MIME_TYPES = ('image/gif', 'image/jpeg', 'image/png')


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
    if min(image.size) < 100:
        message = _("Uploaded image should be at "
                    "least 100 pixels tall and wide.")
        raise ValidationError(message)

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


def crop_string_to_dict(image, crop):
    message = _("Crop is invalid. Please try again.")
    crop_dict = {}

    try:
        crop_list = [int(x) for x in crop.split(',')]
        if len(crop_list) != 8:
            raise ValidationError(message)
    except (TypeError, ValueError):
        raise ValidationError(message)

    cropped_size = (crop_list[0], crop_list[1])

    if cropped_size[0] < 10:
        raise ValidationError(message)
    if cropped_size[1] < 10:
        raise ValidationError(message)

    if crop_list[2] != crop_list[3]:
        # We only allow cropping to squares
        raise ValidationError(message)

    crop_dict['width'] = crop_list[2]
    crop_dict['height'] = crop_list[3]

    if crop_dict['width'] != crop_dict['height']:
        raise ValidationError(message)
    if crop_dict['width'] > cropped_size[0]:
        raise ValidationError(message)
    if crop_dict['height'] > cropped_size[1]:
        raise ValidationError(message)

    crop_dict['source'] = (crop_list[4], crop_list[6],
                           crop_list[5], crop_list[7])

    if crop_dict['source'][0] < 0 or crop_dict['source'][2] > cropped_size[0]:
        raise ValidationError(message)

    if crop_dict['source'][1] < 0 or crop_dict['source'][3] > cropped_size[1]:
        raise ValidationError(message)

    source_w = crop_dict['source'][2] - crop_dict['source'][0]
    source_h = crop_dict['source'][3] - crop_dict['source'][1]

    if source_w != source_h:
        raise ValidationError(message)

    crop_dict['ratio'] = float(image.size[0]) / float(cropped_size[0])

    return crop_dict


def crop_source_image(user, source, crop):
    image = Image.open(store.avatar_file_path(user, source))
    crop = crop_string_to_dict(image, crop)

    crop_dimensions = [int(d * crop['ratio']) for d in crop['source']]
    cropped_image = image.crop(crop_dimensions)

    store.store_avatar(user, cropped_image)
    if source == 'tmp':
        store.store_original_avatar(user)

    return crop


def avatar_source_token(user, source):
    token_seed = (
        unicode(user.pk),
        user.username,
        user.email,
        source,
        unicode(store.avatar_file_path(user, source)),
        settings.SECRET_KEY
    )

    return sha256('+'.join(token_seed)).hexdigest()[:10]


def has_temporary_avatar(user):
    return store.avatar_file_exists(user, 'tmp')


def has_original_avatar(user):
    return store.avatar_file_exists(user, 'org')
