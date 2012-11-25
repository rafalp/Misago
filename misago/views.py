from django.template import RequestContext

def home(request):    
    return request.theme.render_to_response('index.html',
                                            {'page_title': 'Hello World!'},
                                            context_instance=RequestContext(request));

def error403(request, message=None, title=None):
    return error_view(request, 403, message, title)
                                            
def error404(request, message=None, title=None):
    return error_view(request, 404, message, title)

def error_view(request, error, message, title):
    if message:
        message.single = True
    response = request.theme.render_to_response(('error%s.html' % error),
                                            {
                                             'message': message,
                                             'title': title,
                                             'hide_signin': True,
                                             'exception_response': True,
                                             },
                                            context_instance=RequestContext(request));
    response.status_code = error
    return response