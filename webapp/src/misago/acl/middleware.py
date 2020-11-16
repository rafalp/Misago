from . import useracl


def user_acl_middleware(get_response):
    """Sets request.user_acl attribute with dict containing current user acl."""

    def middleware(request):
        request.user_acl = useracl.get_user_acl(request.user, request.cache_versions)
        return get_response(request)

    return middleware
