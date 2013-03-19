from django.template import RequestContext

def error_not_implemented(request, *args, **kwargs):
    """Generic "NOT IMPLEMENTED!" Error"""
    raise NotImplementedError("This action is not implemented!")


def error_view(request, error, message):
    response = request.theme.render_to_response(('error%s.html' % error),
                                                {
                                                 'message': message,
                                                 'hide_signin': True,
                                                 'exception_response': True,
                                                 },
                                                context_instance=RequestContext(request));
    response.status_code = error
    return response


def error403(request, message=None):
    return error_view(request, 403, message)


def error404(request, message=None):
    return error_view(request, 404, message)


def error_banned(request, user=None, ban=None):
    if not ban:
        ban = request.ban
    response = request.theme.render_to_response('error403_banned.html',
                                                {
                                                 'banned_user': user,
                                                 'ban': ban,
                                                 'hide_signin': True,
                                                 'exception_response': True,
                                                 },
                                                context_instance=RequestContext(request));
    response.status_code = 403
    return response