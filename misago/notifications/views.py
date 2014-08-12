from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _, ungettext

from misago.core.uiviews import uiview

from misago.users.decorators import deny_guests


@deny_guests
def notifications(request):
    if request.is_ajax():
        return dropdown(request)
    else:
        return full_page(request)


def dropdown(request):
    template = render(request, 'misago/notifications/dropdown.html', {
        'items': request.user.notifications.order_by('-id').iterator(),
        'notifications_count': request.user.notifications.count(),
    })

    return JsonResponse({
        'is_error': False,
        'count': request.user.new_notifications,
        'html': template.content,
    })


def full_page(request):
    return render(request, 'misago/notifications/full.html')


@uiview('misago_notifications')
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


@deny_guests
def new_notification(request):
    from django.contrib.auth import get_user_model
    from faker import Factory
    faker = Factory.create()

    sender = get_user_model().objects.order_by('?')[:1][0]

    from misago.notifications import notify_user
    notify_user(
        request.user,
        _("Replied to %(thread)s"),
        '/',
        'test',
        formats={'thread': 'LoremIpsum'},
        sender=sender,)

    from django.http import HttpResponse
    return HttpResponse('Notification set.')
