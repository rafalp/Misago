from django.contrib.auth import get_user_model

from ..notifications.tasks import notify_on_new_private_thread
from ..threadupdates.create import (
    create_changed_owner_thread_update,
    create_invited_participant_thread_update,
    create_joined_thread_update,
    create_left_thread_update,
    create_removed_participant_thread_update,
    create_took_ownership_thread_update,
)
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
        create_changed_owner_thread_update(
            thread, new_owner, request.user, request=request
        )
    else:
        create_took_ownership_thread_update(thread, request.user, request=request)


def add_participant(request, thread, new_participant):
    """adds single participant to thread, registers this on the event"""
    add_participants(request.user, thread, [new_participant])

    if request.user == new_participant:
        create_joined_thread_update(thread, request.user, request=request)
    else:
        create_invited_participant_thread_update(
            thread, new_participant, request.user, request=request
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
            thread.is_closed = True
            thread.save(update_fields=["is_closed"])

        if request.user == user:
            create_left_thread_update(thread, request.user, request=request)
        else:
            create_removed_participant_thread_update(
                thread, user, request.user, request=request
            )
