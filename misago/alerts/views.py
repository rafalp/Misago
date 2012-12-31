from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.authn.decorators import block_guest
from misago.views import error404

@block_guest
def show_alerts(request):
    now = timezone.now()
    alerts = {}
    if not request.user.alerts_date:
        request.user.alerts_date = request.user.join_date
    for alert in request.user.alert_set.order_by('-id'):
        alert.new = alert.date > request.user.alerts_date
        diff = now - alert.date
        if diff.days <= 0:
            try:
                alerts['today'].append(alert)
            except KeyError:
                alerts['today'] = [alert]
        elif diff.days <= 1:
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
                alerts['mont'] = [alert]
        else:
            try:
                alerts['older'].append(alert)
            except KeyError:
                alerts['older'] = [alert]
    response = request.theme.render_to_response('alerts.html',
                                                {
                                                 'alerts': alerts
                                                 },
                                                context_instance=RequestContext(request));
    # Sync alerts
    request.user.alerts = 0
    request.user.alerts_date = now
    request.user.save(force_update=True)
    return response