from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.utils.views import json_response

def error_not_implemented(request, *args, **kwargs):
    """Generic "NOT IMPLEMENTED!" Error"""
    raise NotImplementedError("This action is not implemented!")


def error_view(request, error, message):
    if request.is_ajax():
        if not message:
            if error == 404:
                message = _("Requested page could not be loaded.")
            if error == 403:
                message = _("You don't have permission to see requested page.")
        return json_response(request, status=error, message=message)
    response = request.theme.render_to_response(('error%s.html' % error),
                                                {
                                                 'message': unicode(message),
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
    if request.is_ajax():
        return json_response(request, status=403, message=_("You are banned."))
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