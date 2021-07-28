from typing import Any

from misago.users.hooks.updateuser import update_user_hook
from misago.graphql.hooks import graphql_context_hook

print("PLUGIN!", __file__)


@graphql_context_hook.append
async def add_plugin_data_to_graphql_context(action, request):
    context = await action(request)
    context["plugin"] = "YES!"
    return context


@update_user_hook.append
async def update_user_updates_count(next_action: Any, user, **kwargs):
    if not kwargs.get("extra"):
        kwargs["extra"] = user.extra

    kwargs["extra"].setdefault("updates", 0)
    kwargs["extra"]["updates"] += 1
    return await next_action(user, **kwargs)
