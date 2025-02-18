from django.contrib.auth import get_user_model

from ..notifications.tasks import notify_on_new_private_thread
from .events import record_event
from .models import Thread, ThreadParticipant

User = get_user_model()


def has_participants(thread):
    return thread.threadparticipant_set.exists()


def make_participants_aware(user, target):
    if hasattr(target, "__iter__"):
        make_threads_participants_aware(user, target)
    else:
        make_thread_participants_aware(user, target)


def make_threads_participants_aware(user, threads):
    threads_dict = {}
    for thread in threads:
        thread.participant = None
        threads_dict[thread.pk] = thread

    participants_qs = ThreadParticipant.objects.filter(
        user=user, thread_id__in=threads_dict.keys()
    )

    for participant in participants_qs:
        participant.user = user
        threads_dict[participant.thread_id].participant = participant


def make_thread_participants_aware(user, thread):
    thread.participants_list = []
    thread.participant = None

    participants_qs = ThreadParticipant.objects.filter(thread=thread)
    participants_qs = participants_qs.select_related("user")
    for participant in participants_qs.order_by("-is_owner", "user__slug"):
        participant.thread = thread
        thread.participants_list.append(participant)
        if participant.user == user:
            thread.participant = participant
    return thread.participants_list


def set_users_unread_private_threads_sync(
    users=None, participants=None, exclude_user=None
):
    users_ids = []
    if users:
        users_ids += [u.pk for u in users]
    if participants:
        users_ids += [p.user_id for p in participants]
    if exclude_user:
        users_ids = filter(lambda u: u != exclude_user.pk, users_ids)

    if not users_ids:
        return

    User.objects.filter(id__in=set(users_ids)).update(sync_unread_private_threads=True)


def set_owner(thread, user):
    ThreadParticipant.objects.set_owner(thread, user)


def change_owner(request, thread, new_owner):
    ThreadParticipant.objects.set_owner(thread, new_owner)
    set_users_unread_private_threads_sync(
        participants=thread.participants_list, exclude_user=request.user
    )

    if thread.participant and thread.participant.is_owner:
        record_event(
            request,
            thread,
            "changed_owner",
            {
                "user": {
                    "id": new_owner.id,
                    "username": new_owner.username,
                    "url": new_owner.get_absolute_url(),
                }
            },
        )
    else:
        record_event(request, thread, "tookover")


def add_participant(request, thread, new_participant):
    """adds single participant to thread, registers this on the event"""
    add_participants(request.user, thread, [new_participant])

    if request.user == new_participant:
        record_event(request, thread, "entered_thread")
    else:
        record_event(
            request,
            thread,
            "added_participant",
            {
                "user": {
                    "id": new_participant.id,
                    "username": new_participant.username,
                    "url": new_participant.get_absolute_url(),
                }
            },
        )


def add_participants(user: User, thread: Thread, participants: list[User]):
    """
    Add multiple participants to thread, set "recount private threads" flag on them
    notify them about being added to thread.
    """
    ThreadParticipant.objects.add_participants(thread, participants)

    try:
        thread_participants = thread.participants_list
    except AttributeError:
        thread_participants = []

    set_users_unread_private_threads_sync(
        users=participants, participants=thread_participants, exclude_user=user
    )

    private_thread_member_ids = [
        participant.id for participant in participants if participant.id != user.id
    ]

    if private_thread_member_ids:
        notify_on_new_private_thread.delay(
            user.id, thread.id, private_thread_member_ids
        )


def remove_participant(request, thread, user):
    """remove thread participant, set "recound private threads" flag on user"""
    removed_owner = False
    remaining_participants = []

    for participant in thread.participants_list:
        if participant.user == user:
            removed_owner = participant.is_owner
        else:
            remaining_participants.append(participant.user)

    set_users_unread_private_threads_sync(participants=thread.participants_list)

    if not remaining_participants:
        thread.delete()
    else:
        thread.threadparticipant_set.filter(user=user).delete()
        thread.watchedthread_set.filter(user=user).delete()

        if removed_owner:
            thread.is_closed = True  # flag thread to close

            if request.user == user:
                event_type = "owner_left"
            else:
                event_type = "removed_owner"
        else:
            if request.user == user:
                event_type = "participant_left"
            else:
                event_type = "removed_participant"

        record_event(
            request,
            thread,
            event_type,
            {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "url": user.get_absolute_url(),
                }
            },
        )
