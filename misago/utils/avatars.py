from django.conf import settings
try:
    import PIL
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