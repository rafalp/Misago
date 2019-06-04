from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _, ngettext
from rest_framework import serializers
from rest_framework.response import Response

from ....acl import useracl
from ....acl.objectacl import add_acl_to_obj
from ....categories.models import Category
from ....categories.permissions import allow_browse_category, allow_see_category
from ....categories.serializers import CategorySerializer
from ....conf import settings
from ....core.apipatch import ApiPatch
from ....core.shortcuts import get_int_or_404
from ...moderation import threads as moderation
from ...participants import (
    add_participant,
    change_owner,
    make_participants_aware,
    remove_participant,
)
from ...permissions import (
    allow_add_participant,
    allow_add_participants,
    allow_approve_thread,
    allow_change_best_answer,
    allow_change_owner,
    allow_edit_thread,
    allow_hide_thread,
    allow_mark_as_best_answer,
    allow_mark_best_answer,
    allow_move_thread,
    allow_pin_thread,
    allow_remove_participant,
    allow_see_post,
    allow_start_thread,
    allow_unhide_thread,
    allow_unmark_best_answer,
)
from ...serializers import ThreadParticipantSerializer
from ...validators import validate_thread_title

User = get_user_model()

thread_patch_dispatcher = ApiPatch()


def patch_acl(request, thread, value):
    """useful little op that updates thread acl to current state"""
    if value:
        add_acl_to_obj(request.user_acl, thread)
        return {"acl": thread.acl}
    return {"acl": None}


thread_patch_dispatcher.add("acl", patch_acl)


def patch_title(request, thread, value):
    try:
        value_cleaned = str(value).strip()
    except (TypeError, ValueError):
        raise PermissionDenied(_("Not a valid string."))

    try:
        validate_thread_title(request.settings, value_cleaned)
    except ValidationError as e:
        raise PermissionDenied(e.args[0])

    allow_edit_thread(request.user_acl, thread)

    moderation.change_thread_title(request, thread, value_cleaned)
    return {"title": thread.title}


thread_patch_dispatcher.replace("title", patch_title)


def patch_weight(request, thread, value):
    allow_pin_thread(request.user_acl, thread)

    if not thread.acl.get("can_pin_globally") and thread.weight == 2:
        raise PermissionDenied(
            _("You can't change globally pinned threads weights in this category.")
        )

    if value == 2:
        if thread.acl.get("can_pin_globally"):
            moderation.pin_thread_globally(request, thread)
        else:
            raise PermissionDenied(
                _("You can't pin threads globally in this category.")
            )
    elif value == 1:
        moderation.pin_thread_locally(request, thread)
    elif value == 0:
        moderation.unpin_thread(request, thread)

    return {"weight": thread.weight}


thread_patch_dispatcher.replace("weight", patch_weight)


def patch_move(request, thread, value):
    allow_move_thread(request.user_acl, thread)

    category_pk = get_int_or_404(value)
    new_category = get_object_or_404(
        Category.objects.all_categories().select_related("parent"), pk=category_pk
    )

    add_acl_to_obj(request.user_acl, new_category)
    allow_see_category(request.user_acl, new_category)
    allow_browse_category(request.user_acl, new_category)
    allow_start_thread(request.user_acl, new_category)

    if new_category == thread.category:
        raise PermissionDenied(
            _("You can't move thread to the category it's already in.")
        )

    moderation.move_thread(request, thread, new_category)

    return {"category": CategorySerializer(new_category).data}


thread_patch_dispatcher.replace("category", patch_move)


def patch_flatten_categories(request, thread, value):
    try:
        return {"category": thread.category_id}
    except AttributeError:
        return {"category": thread.category_id}


thread_patch_dispatcher.replace("flatten-categories", patch_flatten_categories)


def patch_is_unapproved(request, thread, value):
    allow_approve_thread(request.user_acl, thread)

    if value:
        raise PermissionDenied(_("Content approval can't be reversed."))

    moderation.approve_thread(request, thread)

    return {
        "is_unapproved": thread.is_unapproved,
        "has_unapproved_posts": thread.has_unapproved_posts,
    }


thread_patch_dispatcher.replace("is-unapproved", patch_is_unapproved)


def patch_is_closed(request, thread, value):
    if thread.acl.get("can_close"):
        if value:
            moderation.close_thread(request, thread)
        else:
            moderation.open_thread(request, thread)

        return {"is_closed": thread.is_closed}
    else:
        if value:
            raise PermissionDenied(_("You don't have permission to close this thread."))
        else:
            raise PermissionDenied(_("You don't have permission to open this thread."))


thread_patch_dispatcher.replace("is-closed", patch_is_closed)


def patch_is_hidden(request, thread, value):
    if value:
        allow_hide_thread(request.user_acl, thread)
        moderation.hide_thread(request, thread)
    else:
        allow_unhide_thread(request.user_acl, thread)
        moderation.unhide_thread(request, thread)

    return {"is_hidden": thread.is_hidden}


thread_patch_dispatcher.replace("is-hidden", patch_is_hidden)


def patch_subscription(request, thread, value):
    request.user.subscription_set.filter(thread=thread).delete()

    if value == "notify":
        thread.subscription = request.user.subscription_set.create(
            thread=thread,
            category=thread.category,
            last_read_on=thread.last_post_on,
            send_email=False,
        )

        return {"subscription": False}

    if value == "email":
        thread.subscription = request.user.subscription_set.create(
            thread=thread,
            category=thread.category,
            last_read_on=thread.last_post_on,
            send_email=True,
        )

        return {"subscription": True}

    return {"subscription": None}


thread_patch_dispatcher.replace("subscription", patch_subscription)


def patch_best_answer(request, thread, value):
    try:
        post_id = int(value)
    except (TypeError, ValueError):
        raise PermissionDenied(_("A valid integer is required."))

    allow_mark_best_answer(request.user_acl, thread)

    post = get_object_or_404(thread.post_set, id=post_id)
    post.category = thread.category
    post.thread = thread

    allow_see_post(request.user_acl, post)
    allow_mark_as_best_answer(request.user_acl, post)

    if post.is_best_answer:
        raise PermissionDenied(
            _("This post is already marked as thread's best answer.")
        )

    if thread.has_best_answer:
        allow_change_best_answer(request.user_acl, thread)

    thread.set_best_answer(request.user, post)
    thread.save()

    return {
        "best_answer": thread.best_answer_id,
        "best_answer_is_protected": thread.best_answer_is_protected,
        "best_answer_marked_on": thread.best_answer_marked_on,
        "best_answer_marked_by": thread.best_answer_marked_by_id,
        "best_answer_marked_by_name": thread.best_answer_marked_by_name,
        "best_answer_marked_by_slug": thread.best_answer_marked_by_slug,
    }


thread_patch_dispatcher.replace("best-answer", patch_best_answer)


def patch_unmark_best_answer(request, thread, value):
    try:
        post_id = int(value)
    except (TypeError, ValueError):
        raise PermissionDenied(_("A valid integer is required."))

    post = get_object_or_404(thread.post_set, id=post_id)
    post.category = thread.category
    post.thread = thread

    if not post.is_best_answer:
        raise PermissionDenied(
            _(
                "This post can't be unmarked because "
                "it's not currently marked as best answer."
            )
        )

    allow_unmark_best_answer(request.user_acl, thread)
    thread.clear_best_answer()
    thread.save()

    return {
        "best_answer": None,
        "best_answer_is_protected": False,
        "best_answer_marked_on": None,
        "best_answer_marked_by": None,
        "best_answer_marked_by_name": None,
        "best_answer_marked_by_slug": None,
    }


thread_patch_dispatcher.remove("best-answer", patch_unmark_best_answer)


def patch_add_participant(request, thread, value):
    allow_add_participants(request.user_acl, thread)

    try:
        username = str(value).strip().lower()
        if not username:
            raise PermissionDenied(_("You have to enter new participant's username."))
        participant = User.objects.get(slug=username)
    except User.DoesNotExist:
        raise PermissionDenied(_("No user with such name exists."))

    if participant in [p.user for p in thread.participants_list]:
        raise PermissionDenied(_("This user is already thread participant."))

    participant_acl = useracl.get_user_acl(participant, request.cache_versions)
    allow_add_participant(request.user_acl, participant, participant_acl)
    add_participant(request, thread, participant)

    make_participants_aware(request.user, thread)
    participants = ThreadParticipantSerializer(thread.participants_list, many=True)

    return {"participants": participants.data}


thread_patch_dispatcher.add("participants", patch_add_participant)


def patch_remove_participant(request, thread, value):
    # pylint: disable=undefined-loop-variable
    try:
        user_id = int(value)
    except (ValueError, TypeError):
        raise PermissionDenied(_("A valid integer is required."))

    for participant in thread.participants_list:
        if participant.user_id == user_id:
            break
    else:
        raise PermissionDenied(_("Participant doesn't exist."))

    allow_remove_participant(request.user_acl, thread, participant.user)
    remove_participant(request, thread, participant.user)

    if len(thread.participants_list) == 1:
        return {"deleted": True}

    make_participants_aware(request.user, thread)
    participants = ThreadParticipantSerializer(thread.participants_list, many=True)

    return {"deleted": False, "participants": participants.data}


thread_patch_dispatcher.remove("participants", patch_remove_participant)


def patch_replace_owner(request, thread, value):
    # pylint: disable=undefined-loop-variable
    try:
        user_id = int(value)
    except (ValueError, TypeError):
        raise PermissionDenied(_("A valid integer is required."))

    for participant in thread.participants_list:
        if participant.user_id == user_id:
            if participant.is_owner:
                raise PermissionDenied(_("This user already is thread owner."))
            else:
                break
    else:
        raise PermissionDenied(_("Participant doesn't exist."))

    allow_change_owner(request.user_acl, thread)
    change_owner(request, thread, participant.user)

    make_participants_aware(request.user, thread)
    participants = ThreadParticipantSerializer(thread.participants_list, many=True)
    return {"participants": participants.data}


thread_patch_dispatcher.replace("owner", patch_replace_owner)


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
        thread.category.save(update_fields=["last_thread_title", "last_thread_slug"])

    return response


def bulk_patch_endpoint(
    request, viewmodel
):  # pylint: disable=too-many-branches, too-many-locals
    serializer = BulkPatchSerializer(
        data=request.data, context={"settings": request.settings}
    )
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    threads = clean_threads_for_patch(request, viewmodel, serializer.data["ids"])

    old_titles = [t.title for t in threads]
    old_is_hidden = [t.is_hidden for t in threads]
    old_is_unapproved = [t.is_unapproved for t in threads]
    old_category = [t.category_id for t in threads]

    response = thread_patch_dispatcher.dispatch_bulk(request, threads)

    new_titles = [t.title for t in threads]
    new_is_hidden = [t.is_hidden for t in threads]
    new_is_unapproved = [t.is_unapproved for t in threads]
    new_category = [t.category_id for t in threads]

    # sync titles
    if new_titles != old_titles:
        for i, t in enumerate(threads):
            if t.title != old_titles[i] and t.category.last_thread_id == t.pk:
                t.category.last_thread_title = t.title
                t.category.last_thread_slug = t.slug
                t.category.save(update_fields=["last_thread_title", "last_thread_slug"])

    # sync categories
    sync_categories = []

    if new_is_hidden != old_is_hidden:
        for i, t in enumerate(threads):
            if t.is_hidden != old_is_hidden[i] and t.category_id not in sync_categories:
                sync_categories.append(t.category_id)

    if new_is_unapproved != old_is_unapproved:
        for i, t in enumerate(threads):
            if (
                t.is_unapproved != old_is_unapproved[i]
                and t.category_id not in sync_categories
            ):
                sync_categories.append(t.category_id)

    if new_category != old_category:
        for i, t in enumerate(threads):
            if t.category_id != old_category[i]:
                if t.category_id not in sync_categories:
                    sync_categories.append(t.category_id)
                if old_category[i] not in sync_categories:
                    sync_categories.append(old_category[i])

    if sync_categories:
        for category in Category.objects.filter(id__in=sync_categories):
            category.synchronize()
            category.save()

    return response


def clean_threads_for_patch(request, viewmodel, threads_ids):
    threads = []
    for thread_id in sorted(set(threads_ids), reverse=True):
        try:
            threads.append(viewmodel(request, thread_id).unwrap())
        except (Http404, PermissionDenied):
            raise PermissionDenied(
                _("One or more threads to update could not be found.")
            )
    return threads


class BulkPatchSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1), min_length=1
    )
    ops = serializers.ListField(
        child=serializers.DictField(), min_length=1, max_length=10
    )

    def validate_ids(self, data):
        limit = self.context["settings"].threads_per_page
        if len(data) > limit:
            message = ngettext(
                "No more than %(limit)s thread can be updated at a single time.",
                "No more than %(limit)s threads can be updated at a single time.",
                limit,
            )
            raise ValidationError(message % {"limit": limit})
        return data
