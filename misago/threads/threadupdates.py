from typing import TYPE_CHECKING, Union

from django.db.models import Model
from django.http import HttpRequest
from django.utils import timezone

from .hooks import (
    create_thread_update_hook,
    delete_thread_update_hook,
    hide_thread_update_hook,
    unhide_thread_update_hook,
)
from .models import Thread, ThreadUpdate

if TYPE_CHECKING:
    from ..users.models import User

__all__ = [
    "create_thread_update",
    "delete_thread_update",
    "hide_thread_update",
    "unhide_thread_update",
]


def create_thread_update(
    thread: Thread,
    action: str,
    actor: Union["User", None, str] = None,
    *,
    request: HttpRequest | None = None,
    context: str | None = None,
    context_object: Model | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update_hook(
        _create_thread_update_action,
        thread,
        action,
        actor,
        request=request,
        context=context,
        context_object=context_object,
        is_hidden=is_hidden,
        plugin_data={},
    )


def _create_thread_update_action(
    thread: Thread,
    action: str,
    actor: Union["User", None, str] = None,
    *,
    request: HttpRequest | None = None,
    context: str | None = None,
    context_object: Model | None = None,
    is_hidden: bool = False,
    plugin_data: dict,
) -> ThreadUpdate:
    actor_id = None
    actor_name = None
    context_type = None
    context_id = None

    if isinstance(actor, str):
        actor_name = actor
    elif actor:
        actor_id = actor.id
        actor_name = actor.username

    if context_object:
        context_type = ".".join(
            (
                context_object._meta.app_label,
                context_object._meta.model_name,
            )
        )
        context_id = context_object.id

    return ThreadUpdate.objects.create(
        category_id=thread.category_id,
        thread_id=thread.id,
        actor_id=actor_id,
        actor_name=actor_name,
        action=action,
        context=context,
        context_type=context_type,
        context_id=context_id,
        created_at=timezone.now(),
        is_hidden=is_hidden,
        plugin_data=plugin_data,
    )


def hide_thread_update(
    thread_update: ThreadUpdate, request: HttpRequest | None = None
) -> bool:
    return hide_thread_update_hook(
        _hide_thread_update_action, thread_update, {"is_hidden", "hidden_at"}, request
    )


def _hide_thread_update_action(
    thread_update: ThreadUpdate,
    update_fields: set[str],
    request: HttpRequest | None = None,
) -> bool:
    if thread_update.is_hidden:
        return False

    thread_update.is_hidden = True
    thread_update.hidden_at = timezone.now()

    if request and request.user.is_authenticated:
        thread_update.hidden_by = request.user
        thread_update.hidden_by_name = request.user.username
        update_fields.update(("hidden_by", "hidden_by_name"))

    thread_update.save(update_fields=update_fields)
    return True


def unhide_thread_update(
    thread_update: ThreadUpdate, request: HttpRequest | None = None
) -> bool:
    return unhide_thread_update_hook(
        _unhide_thread_update_action, thread_update, {"is_hidden", "hidden_at"}, request
    )


def _unhide_thread_update_action(
    thread_update: ThreadUpdate,
    update_fields: set[str],
    request: HttpRequest | None = None,
) -> bool:
    if not thread_update.is_hidden:
        return False

    thread_update.is_hidden = False
    thread_update.hidden_by = None
    thread_update.hidden_by_name = None
    thread_update.hidden_at = None

    update_fields.update(("hidden_by", "hidden_by_name"))

    thread_update.save(update_fields=update_fields)
    return True


def delete_thread_update(
    thread_update: ThreadUpdate, request: HttpRequest | None = None
):
    delete_thread_update_hook(_delete_thread_update_action, thread_update, request)


def _delete_thread_update_action(
    thread_update: ThreadUpdate, request: HttpRequest | None = None
):
    thread_update.delete()
    return True
