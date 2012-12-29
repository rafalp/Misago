from django.conf import settings
try:
    from PIL import Image
    has_pil = True
except ImportError:
    has_pil = False

avatar_sizes = {}
def avatar_size(size):
    if not has_pil:
        return None
    try:
        return avatar_sizes[size]
    except KeyError:
        avatar_sizes[size] = None
        for i in settings.AVATAR_SIZES[1:]:
            if size <= i:
                avatar_sizes[size] = i
    return avatar_sizes[size]


def resizeimage(image, size, target):
    if isinstance(image, basestring):
        image = Image.open(image)
    info = image.info
    format = image.format
    if format in "GIF":
        if 'transparency' in info:
            image = image.resize((size, size), Image.ANTIALIAS)
            image.save(target, image.format, transparency=info['transparency'])
        else:
            image = image.convert("RGB")
            image = image.resize((size, size), Image.ANTIALIAS)
            image = image.convert('P', palette=Image.ADAPTIVE)
            image.save(target, image.format)
    if format in "PNG":
        image = image.resize((size, size), Image.ANTIALIAS)
        image.save(target, quality=95)
    if format == "JPEG":
        image = image.convert("RGB")
        image = image.resize((size, size), Image.ANTIALIAS) 
        image = image.convert('P', palette=Image.ADAPTIVE)
        image = image.convert("RGB", dither=None)
        image.save(target, image.format, quality=95)