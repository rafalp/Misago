from django.core.urlresolvers import reverse


def _compare_path_under_to_forum_index(request):
    forum_index = reverse('forum_index')
    path_info = request.path_info

    if len(forum_index) > len(path_info):
        return False
    return path_info[:len(forum_index)] == forum_index


def is_request_to_misago(request):
    """Is request directed at Misago instead of... say, CMS app?"""
    try:
        return request._request_to_misago
    except AttributeError:
        request._request_to_misago = _compare_path_under_to_forum_index(request)
        return request._request_to_misago

