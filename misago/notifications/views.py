from django.contrib import messages
from django.db.transaction import atomic
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _, ungettext

from misago.core.uiviews import uiview
from misago.users.decorators import deny_guests

from misago.notifications import (read_all_user_alerts,
                                  assert_real_new_notifications_count)
from misago.notifications.models import Notification


@deny_guests
def notifications(request):
    if request.method == 'POST':
        if 'read-all' in request.POST:
            return read_all(request)
        if request.POST.get('notification'):
            return read_notification(request)
    else:
        assert_real_new_notifications_count(request.user)

    if request.is_ajax():
        return dropdown(request)
    else:
        return full_page(request)


def dropdown(request):
    template = render(request, 'misago/notifications/dropdown.html', {
        'notifications_count': request.user.misago_notifications.count(),
        'items': request.user.misago_notifications.order_by('-id')[:15],
    })

    return JsonResponse({
        'is_error': False,
        'count': request.user.new_notifications,
        'html': template.content,
    })


def full_page(request):
    return render(request, 'misago/notifications/full.html', {
        'notifications_count': request.user.misago_notifications.count(),
        'items': request.user.misago_notifications.order_by('-id'),
    })


@atomic
def go_to_notification(request, notification_id, hash):
    queryset = request.user.misago_notifications.select_for_update()
    notification = get_object_or_404(
        queryset, pk=notification_id, hash=hash)

    if notification.is_new:
        update_qs = request.user.misago_notifications.filter(hash=hash)
        update_qs.update(is_new=False)
        assert_real_new_notifications_count(request.user)

    return redirect(notification.url)


@atomic
def read_all(request):
    messages.success(request, _("All notifications were set as read."))
    read_all_user_alerts(request.user)


@atomic
def read_notification(request):
    try:
        queryset = request.user.misago_notifications
        notification = queryset.get(id=request.POST['notification'])

        if notification.is_new:
            is_changed = True
            with atomic():
                notification.is_new = False
                notification.save(update_fields=['is_new'])
                assert_real_new_notifications_count(request.user)
        else:
            is_changed = False

        if request.is_ajax():
            return JsonResponse({
                'is_error': False,
                'is_changed': is_changed
            })
        else:
            messages.success(request, _("Notification was marked as read."))
            return redirect('misago:notifications')
    except Notification.DoesNotExist:
        message = _("Specified notification could not be found.")
        if request.is_ajax():
            return JsonResponse({
                'is_error': True,
                'message': message,
            })
        else:
            messages.error(request, message)
            return redirect('misago:notifications')


@atomic
def read_all(request):
    if not request.is_ajax():
        messages.success(request, _("All notifications were set as read."))
    read_all_user_alerts(request.user)
    return redirect('misago:notifications')


@uiview('notifications')
@deny_guests
def event_sender(request, resolver_match):
    if request.user.new_notifications:
        message = ungettext("%(notifications)s new notification",
                            "%(notifications)s new notifications",
                            request.user.new_notifications)
        message = message % {'notifications': request.user.new_notifications}
    else:
        message = _("Your notifications")

    return {
        'count': request.user.new_notifications,
        'message': message,
    }
