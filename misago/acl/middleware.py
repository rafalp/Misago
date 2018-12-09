from django.utils.functional import SimpleLazyObject

from . import useracl


def user_acl_middleware(get_response):
    """Sets request.cache_versions attribute with dict of cache versions."""
    def middleware(request):
        request.user_acl = useracl.get_user_acl(request.user, request.cache_versions)
        return get_response(request)

    return middleware
