from ..users.groupsproxy import GroupsProxy


def groups_middleware(get_response):
    def middleware(request):
        request.groups = GroupsProxy(request.cache_versions)
        return get_response(request)

    return middleware
