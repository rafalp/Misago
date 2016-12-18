from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

from misago.core.mail import build_mail, send_messages

from .events import record_event
from .models import ThreadParticipant
from .signals import remove_thread_participant


def has_participants(thread):
    return thread.threadparticipant_set.exists()


def make_participants_aware(user, thread):
    thread.participants_list = []
    thread.participant = None

    participants_qs = ThreadParticipant.objects.filter(thread=thread)
    participants_qs = participants_qs.select_related('user')
    for participant in participants_qs.order_by('-is_owner', 'user__slug'):
        participant.thread = thread
        thread.participants_list.append(participant)
        if participant.user == user:
            thread.participant = participant
    return thread.participants_list


def set_owner(thread, user):
    """
    Remove user's ownership over thread
    """
    ThreadParticipant.objects.set_owner(thread, user)


def set_users_unread_private_threads_sync(users):
    User = get_user_model()
    User.objects.filter(id__in=[u.pk for u in users]).update(
        sync_unread_private_threads=True
    )


def add_participant(request, thread, user):
    """
    Adds single participant to thread, registers this on the event
    """
    add_participants(request, thread, [user])
    record_event(request, thread, 'added_participant', {
        'user': {
            'username': user.username,
            'url': user.get_absolute_url(),
        }
    })


def add_participants(request, thread, users):
    """
    Add multiple participants to thread, set "recound private threads" flag on them
    notify them about being added to thread
    """
    ThreadParticipant.objects.add_participants(thread, users)
    set_users_unread_private_threads_sync(users)

    emails = []
    for user in users:
        emails.append(build_noticiation_email(request, thread, user))
    send_messages(emails)


def build_noticiation_email(request, thread, user):
    subject = _('%(user)s has invited you to participate in private thread "%(thread)s"')
    subject_formats = {
        'thread': thread.title,
        'user': request.user.username
    }

    return build_mail(
        request,
        user,
        subject % subject_formats,
        'misago/emails/privatethread/added',
        {
            'thread': thread
        }
    )


def remove_participant(thread, user):
    """
    Remove thread participant, set "recound private threads" flag on user
    """
    thread.threadparticipant_set.filter(user=user).delete()
    set_users_unread_private_threads_sync([user])

    remove_thread_participant.send(thread, user=user)
