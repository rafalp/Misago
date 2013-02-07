from datetime import timedelta
from django.core.urlresolvers import reverse
from django.db.models import F
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.alerts.models import Alert
from misago.authn.decorators import block_guest
from misago.forms import FormLayout
from misago.messages import Message
from misago.users.models import User
from misago.usercp.template import RequestContext
from misago.usercp.models import UsernameChange
from misago.usercp.username.forms import UsernameChangeForm
from misago.views import error404
from misago.utils import ugettext_lazy

@block_guest
def username(request):
    if not request.acl.usercp.show_username_change():
        return error404(request)

    changes_left = request.acl.usercp.changes_left(request.user)

    next_change = None
    if request.acl.usercp.changes_expire() and not changes_left:
        next_change = request.user.namechanges.filter(
                                                      date__gte=timezone.now() - timedelta(days=request.acl.usercp.acl['changes_expire']),
                                                      ).order_by('-date')[0]
        next_change = next_change.date + timedelta(days=request.acl.usercp.acl['changes_expire'])

    message = request.messages.get_message('usercp_username')
    if request.method == 'POST':
        org_username = request.user.username
        form = UsernameChangeForm(request.POST, request=request)
        if form.is_valid():
            request.user.set_username(form.cleaned_data['username'])
            request.user.save(force_update=True)
            request.user.namechanges.create(date=timezone.now(), old_username=org_username)
            request.messages.set_flash(Message(_("Your username has been changed.")), 'success', 'usercp_username')
            # Alert followers of namechange
            alert_time = timezone.now()
            bulk_alerts = []
            alerted_users = []
            for follower in request.user.follows_set.iterator():
                alerted_users.append(follower.pk)
                alert = Alert(user=follower, message=ugettext_lazy("User that you are following, %(username)s, has changed his name to %(newname)s").message, date=alert_time)
                alert.strong('username', org_username)
                alert.profile('newname', request.user)
                alert.hydrate()
                bulk_alerts.append(alert)
            if bulk_alerts:
                Alert.objects.bulk_create(bulk_alerts)
                User.objects.filter(id__in=alerted_users).update(alerts=F('alerts') + 1)
            # Hop back
            return redirect(reverse('usercp_username'))
        message = Message(form.non_field_errors()[0], 'error')
    else:
        form = UsernameChangeForm(request=request)

    return request.theme.render_to_response('usercp/username.html',
                                            context_instance=RequestContext(request, {
                                             'message': message,
                                             'changes_left': changes_left,
                                             'form': FormLayout(form),
                                             'next_change': next_change,
                                             'changes_history': request.user.namechanges.order_by('-date')[:10],
                                             'tab': 'username',
                                             }));
