from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext

def redirect_message(request, message, type='info', owner=None):
    """
    Set flash message and redirect to board index.
    """
    request.messages.set_flash(message, type, owner)
    return redirect(reverse('index'))


"""
Error views
"""
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
