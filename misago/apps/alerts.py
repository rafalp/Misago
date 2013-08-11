from copy import deepcopy
from datetime import timedelta
from django.template import RequestContext
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.translation import ugettext as _
from misago.decorators import block_guest
from misago.shortcuts import render_to_response

@block_guest
def alerts(request):
    now = localtime(timezone.now())
    yesterday = now - timedelta(days=1)
    alerts = {}
    if not request.user.alerts_date:
        request.user.alerts_date = request.user.join_date

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
    return render_to_response('alerts.html',
                              {
                              'new_alerts': new_alerts,
                              'alerts': alerts,
                              },
                              context_instance=RequestContext(request))
