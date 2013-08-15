from copy import deepcopy
from datetime import timedelta
from django.template import RequestContext
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.translation import ugettext as _
from misago.apps.errors import error404
from misago.decorators import block_guest, check_csrf
from misago.shortcuts import render_to_response, json_response
from misago.template.loader import render_to_string

@block_guest
def alerts(request):
    if request.is_ajax():
        if request.session.get('recent_alerts'):
            alerts_qs = request.user.alert_set.filter(date__gte=request.session['recent_alerts']).order_by('-id')
        else:
            alerts_qs = ()
        response_html = render_to_string('alerts/modal.html',
                                         {'alerts': alerts_qs},
                                         context_instance=RequestContext(request))
        if request.user.alerts_date:
            request.user.alerts = 0
            request.user.alerts_date = timezone.now()
            request.user.save(force_update=True)
        return json_response(request,
                             json={'html': response_html})

    if not request.user.alerts_date:
        request.user.alerts_date = request.user.join_date

    now = localtime(timezone.now())
    yesterday = now - timedelta(days=1)
    alerts = {}

    for alert in request.user.alert_set.order_by('-id'):
        alert.new = alert.date > request.user.alerts_date
        alert_date = localtime(deepcopy(alert.date))
        diff = now - alert_date
        if now.date() == alert_date.date():
            try:
                alerts['today'].append(alert)
            except KeyError:
                alerts['today'] = [alert]
        elif yesterday.date() == alert_date.date():
            try:
                alerts['yesterday'].append(alert)
            except KeyError:
                alerts['yesterday'] = [alert]
        elif diff.days <= 7:
            try:
                alerts['week'].append(alert)
            except KeyError:
                alerts['week'] = [alert]
        elif diff.days <= 30:
            try:
                alerts['month'].append(alert)
            except KeyError:
                alerts['month'] = [alert]
        else:
            try:
                alerts['older'].append(alert)
            except KeyError:
                alerts['older'] = [alert]

    new_alerts = request.user.alerts
    request.user.alerts = 0
    request.user.alerts_date = now
    request.user.save(force_update=True)
    return render_to_response('alerts/list.html',
                              {
                              'new_alerts': new_alerts,
                              'alerts': alerts,
                              },
                              context_instance=RequestContext(request))


@block_guest
@check_csrf
def clear_recent(request):
    if not request.is_ajax() or not request.method == 'POST':
        return error404(request)

    del request.session['recent_alerts']
    response_html = render_to_string('alerts/cleared.html',
                                     context_instance=RequestContext(request))
    return json_response(request,
                         json={'html': response_html})