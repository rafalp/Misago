from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext


def home(request):
    return request.theme.render_to_response('index.html',
                                        {'page_title': 'Hello World!'},
                                        context_instance=RequestContext(request));


def redirect_message(request, message, type='info', owner=None):
    request.messages.set_flash(message, type, owner)
    return redirect(reverse('index'))


def error403(request, message=None):
    return error_view(request, 403, message)

                                            
def error404(request, message=None):
    return error_view(request, 404, message)


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