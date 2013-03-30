from json import dumps as json_dumps
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import RequestContext

def redirect_message(request, message, type='info', owner=None):
    request.messages.set_flash(message, type, owner)
    return redirect(reverse('index'))


def json_response(request, json={}, status=200, message=None):
    json.update({'code': status, 'message': unicode(message)})
    response = json_dumps(json, sort_keys=True,  ensure_ascii=False)
    return HttpResponse(response, content_type='application/json', status=status)


def ajax_response(request, template=None, macro=None, vars={}, json={}, status=200, message=None):
    html = ''
    if macro:
        html = request.theme.macro(template, macro, vars, context_instance=RequestContext(request));
    return json_response(request, json.update({'html': html}), status, message)