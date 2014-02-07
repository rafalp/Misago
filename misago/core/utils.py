from django.core.urlresolvers import reverse


def _is_request_path_under_misago(request):
    # We are assuming that forum_index link is root of all Misago links
    forum_index = reverse('misago:index')
    path_info = request.path_info

    if len(forum_index) > len(path_info):
        return False
    return path_info[:len(forum_index)] == forum_index


def is_request_to_misago(request):
    try:
        return request._request_to_misago
    except AttributeError:
        request._request_to_misago = _is_request_path_under_misago(request)
        return request._request_to_misago
