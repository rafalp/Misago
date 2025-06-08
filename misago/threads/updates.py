from typing import TYPE_CHECKING, Union

from django.db.models import Model
from django.utils import timezone

from .models import Thread, ThreadUpdate

if TYPE_CHECKING:
    from ..users.models import User


def create_thread_update(
    thread: Thread,
    action: str,
    actor: Union["User", None, str] = None,
    *,
    context: str | None = None,
    context_object: Model | None = None,
    is_hidden: bool = False,
):
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
    )
