from django.contrib import messages
from django.db.transaction import atomic
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _, ungettext

from misago.core.uiviews import uiview
from misago.users.decorators import deny_guests

from misago.notifications import (read_all_user_alerts,
                                  assert_real_new_notifications_count)


@deny_guests
def notifications(request):
    if request.method == 'POST':
        read_all(request)
        if not request.is_ajax():
            return redirect('misago:notifications')
    else:
        assert_real_new_notifications_count(request.user)

    if request.is_ajax():
        return dropdown(request)
    else:
        return full_page(request)


def dropdown(request):
    template = render(request, 'misago/notifications/dropdown.html', {
        'notifications_count': request.user.notifications.count(),
        'items': request.user.notifications.order_by('-id')[:15],
    })

    return JsonResponse({
        'is_error': False,
        'count': request.user.new_notifications,
        'html': template.content,
    })


def full_page(request):
    return render(request, 'misago/notifications/full.html', {
        'notifications_count': request.user.notifications.count(),
        'items': request.user.notifications.order_by('-id'),
    })


@atomic
def read_all(request):
    if not request.is_ajax():
        messages.success(request, _("All notifications were set as read."))
    read_all_user_alerts(request.user)


@uiview('misago_notifications')
@deny_guests
def event_sender(request, resolver_match):
    if request.user.new_notifications:
        message = ungettext("You have %(notifications)s new notification",
                            "You have %(notifications)s new notifications",
                            request.user.new_notifications)
        message = message % {'notifications': request.user.new_notifications}
    else:
        message = _("Your notifications")

    return {
        'count': request.user.new_notifications,
        'message': message,
    }
