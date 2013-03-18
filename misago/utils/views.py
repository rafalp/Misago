from json import dumps as json_dumps
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import RequestContext

def redirect_message(request, message, type='info', owner=None):
    """
    Set flash message and redirect to board index.
    """
    request.messages.set_flash(message, type, owner)
    return redirect(reverse('index'))


def ajax_response(request, template=None, macro=None, vars={}, json={}, status=200, message=None):
    html = ''
    if macro:
        html = request.theme.macro(template, macro, vars, context_instance=RequestContext(request));
    response = json_dumps(dict(json.items() + {
                                       'code': status,
                                       'message': message,
                                       'html': html
                                       }.items()), sort_keys=True,  ensure_ascii=False)
    return HttpResponse(response, content_type='application/json', status=status)