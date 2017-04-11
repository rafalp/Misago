from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404
from django.utils import six
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.categories.models import Category
from misago.categories.permissions import allow_browse_category, allow_see_category
from misago.categories.serializers import CategorySerializer
from misago.core.apipatch import ApiPatch
from misago.core.shortcuts import get_int_or_404
from misago.threads.moderation import threads as moderation
from misago.threads.participants import (
    add_participant, change_owner, make_participants_aware, remove_participant)
from misago.threads.permissions import (
    allow_add_participant, allow_add_participants, allow_change_owner, allow_edit_thread,
    allow_remove_participant, allow_start_thread)
from misago.threads.serializers import ThreadParticipantSerializer
from misago.threads.validators import validate_title


UserModel = get_user_model()

thread_patch_dispatcher = ApiPatch()


def patch_acl(request, thread, value):
    """useful little op that updates thread acl to current state"""
    if value:
        add_acl(request.user, thread)
        return {'acl': thread.acl}
    else:
        return {'acl': None}


thread_patch_dispatcher.add('acl', patch_acl)


def patch_title(request, thread, value):
    try:
        value_cleaned = six.text_type(value).strip()
    except (TypeError, ValueError):
        raise PermissionDenied(_("Invalid thread title."))

    try:
        validate_title(value_cleaned)
    except ValidationError as e:
        raise PermissionDenied(e.args[0])

    allow_edit_thread(request.user, thread)

    moderation.change_thread_title(request, thread, value_cleaned)
    return {'title': thread.title}


thread_patch_dispatcher.replace('title', patch_title)


def patch_weight(request, thread, value):
    message = _("You don't have permission to change this thread's weight.")
    if not thread.acl.get('can_pin'):
        raise PermissionDenied(message)
    elif thread.weight > thread.acl.get('can_pin'):
        raise PermissionDenied(message)

    if value == 2:
        if thread.acl.get('can_pin') == 2:
            moderation.pin_thread_globally(request, thread)
        else:
            raise PermissionDenied(_("You don't have permission to pin this thread globally."))
    elif value == 1:
        moderation.pin_thread_locally(request, thread)
    elif value == 0:
        moderation.unpin_thread(request, thread)

    return {'weight': thread.weight}


thread_patch_dispatcher.replace('weight', patch_weight)


def patch_move(request, thread, value):
    if not thread.acl.get('can_move'):
        raise PermissionDenied(_("You don't have permission to move this thread."))

    category_pk = get_int_or_404(value)
    new_category = get_object_or_404(
        Category.objects.all_categories().select_related('parent'), pk=category_pk
    )

    add_acl(request.user, new_category)
    allow_see_category(request.user, new_category)
    allow_browse_category(request.user, new_category)
    allow_start_thread(request.user, new_category)

    if new_category == thread.category:
        raise PermissionDenied(_("You can't move thread to the category it's already in."))

    moderation.move_thread(request, thread, new_category)

    return {'category': CategorySerializer(new_category).data}


thread_patch_dispatcher.replace('category', patch_move)


def patch_flatten_categories(request, thread, value):
    try:
        return {'category': thread.category_id}
    except AttributeError:
        return {'category': thread.category_id}


thread_patch_dispatcher.replace('flatten-categories', patch_flatten_categories)


def patch_is_unapproved(request, thread, value):
    if thread.acl.get('can_approve'):
        if value:
            raise PermissionDenied(_("Content approval can't be reversed."))

        moderation.approve_thread(request, thread)

        return {
            'is_unapproved': thread.is_unapproved,
            'has_unapproved_posts': thread.has_unapproved_posts,
        }
    else:
        raise PermissionDenied(_("You don't have permission to approve this thread."))


thread_patch_dispatcher.replace('is-unapproved', patch_is_unapproved)


def patch_is_closed(request, thread, value):
    if thread.acl.get('can_close'):
        if value:
            moderation.close_thread(request, thread)
        else:
            moderation.open_thread(request, thread)

        return {'is_closed': thread.is_closed}
    else:
        if value:
            raise PermissionDenied(_("You don't have permission to close this thread."))
        else:
            raise PermissionDenied(_("You don't have permission to open this thread."))


thread_patch_dispatcher.replace('is-closed', patch_is_closed)


def patch_is_hidden(request, thread, value):
    if thread.acl.get('can_hide'):
        if value:
            moderation.hide_thread(request, thread)
        else:
            moderation.unhide_thread(request, thread)

        return {'is_hidden': thread.is_hidden}
    else:
        raise PermissionDenied(_("You don't have permission to hide this thread."))


thread_patch_dispatcher.replace('is-hidden', patch_is_hidden)


def patch_subscription(request, thread, value):
    request.user.subscription_set.filter(thread=thread).delete()

    if value == 'notify':
        thread.subscription = request.user.subscription_set.create(
            thread=thread,
            category=thread.category,
            last_read_on=thread.last_post_on,
            send_email=False,
        )

        return {'subscription': False}
    elif value == 'email':
        thread.subscription = request.user.subscription_set.create(
            thread=thread,
            category=thread.category,
            last_read_on=thread.last_post_on,
            send_email=True,
        )

        return {'subscription': True}
    else:
        return {'subscription': None}


thread_patch_dispatcher.replace('subscription', patch_subscription)


def patch_add_participant(request, thread, value):
    allow_add_participants(request.user, thread)

    try:
        username = six.text_type(value).strip().lower()
        if not username:
            raise PermissionDenied(_("You have to enter new participant's username."))
        participant = UserModel.objects.get(slug=username)
    except UserModel.DoesNotExist:
        raise PermissionDenied(_("No user with such name exists."))

    if participant in [p.user for p in thread.participants_list]:
        raise PermissionDenied(_("This user is already thread participant."))

    allow_add_participant(request.user, participant)
    add_participant(request, thread, participant)

    make_participants_aware(request.user, thread)
    participants = ThreadParticipantSerializer(thread.participants_list, many=True)

    return {'participants': participants.data}


thread_patch_dispatcher.add('participants', patch_add_participant)


def patch_remove_participant(request, thread, value):
    try:
        user_id = int(value)
    except (ValueError, TypeError):
        user_id = 0

    for participant in thread.participants_list:
        if participant.user_id == user_id:
            break
    else:
        raise PermissionDenied(_("Participant doesn't exist."))

    allow_remove_participant(request.user, thread, participant.user)
    remove_participant(request, thread, participant.user)

    if len(thread.participants_list) == 1:
        return {'deleted': True}
    else:
        make_participants_aware(request.user, thread)
        participants = ThreadParticipantSerializer(thread.participants_list, many=True)

        return {
            'deleted': False,
            'participants': participants.data,
        }


thread_patch_dispatcher.remove('participants', patch_remove_participant)


def patch_replace_owner(request, thread, value):
    try:
        user_id = int(value)
    except (ValueError, TypeError):
        user_id = 0

    for participant in thread.participants_list:
        if participant.user_id == user_id:
            if participant.is_owner:
                raise PermissionDenied(_("This user already is thread owner."))
            else:
                break
    else:
        raise PermissionDenied(_("Participant doesn't exist."))

    allow_change_owner(request.user, thread)
    change_owner(request, thread, participant.user)

    make_participants_aware(request.user, thread)
    participants = ThreadParticipantSerializer(thread.participants_list, many=True)
    return {'participants': participants.data}


thread_patch_dispatcher.replace('owner', patch_replace_owner)


def thread_patch_endpoint(request, thread):
    old_title = thread.title
    old_is_hidden = thread.is_hidden
    old_is_unapproved = thread.is_unapproved
    old_category = thread.category

    response = thread_patch_dispatcher.dispatch(request, thread)

    # diff thread's state against pre-patch and resync category if necessary
    hidden_changed = old_is_hidden != thread.is_hidden
    unapproved_changed = old_is_unapproved != thread.is_unapproved
    category_changed = old_category != thread.category

    title_changed = old_title != thread.title
    if thread.category.last_thread_id != thread.pk:
        title_changed = False  # don't trigger resync on simple title change

    if hidden_changed or unapproved_changed or category_changed:
        thread.category.synchronize()
        thread.category.save()

        if category_changed:
            old_category.synchronize()
            old_category.save()
    elif title_changed:
        thread.category.last_thread_title = thread.title
        thread.category.last_thread_slug = thread.slug
        thread.category.save(update_fields=['last_thread_title', 'last_thread_slug'])

    return response
