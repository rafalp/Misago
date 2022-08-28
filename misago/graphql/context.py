from dataclasses import dataclass

from starlette.requests import Request

from ..auth import get_authenticated_admin, get_authenticated_user
from ..cacheversions import get_cache_versions
from ..categories.index import get_categories_index
from ..categories.loaders import categories_children_loader, categories_loader
from ..conf.dynamicsettings import get_dynamic_settings
from ..context import Context
from ..permissions.users import get_user_permissions, get_anonymous_permissions
from ..threads.loaders import posts_loader, threads_loader
from ..users.loaders import users_groups_loader, users_loader
from ..users.models import User
from .hooks import graphql_context_hook


@dataclass
class Space:
    admin: bool
    public: bool


async def get_admin_graphql_context(request: Request) -> Context:
    return await graphql_context_hook.call_action(
        get_admin_graphql_context_action, request
    )


async def get_admin_graphql_context_action(request: Request) -> Context:
    context = await get_graphql_context(request)
    context["space"] = Space(admin=True, public=False)
    context["user"] = await get_authenticated_admin(context)
    context["permissions"] = await get_permissions(context)
    request.scope["user"] = context["user"]
    return context


async def get_public_graphql_context(request: Request) -> Context:
    return await graphql_context_hook.call_action(
        get_public_graphql_context_action, request
    )


async def get_public_graphql_context_action(request: Request) -> Context:
    context = await get_graphql_context(request)
    context["space"] = Space(admin=False, public=True)
    context["user"] = await get_authenticated_user(context)
    context["permissions"] = await get_permissions(context)
    request.scope["user"] = context["user"]
    return context


async def get_graphql_context(request: Request) -> Context:
    request.scope["user"] = None

    context: Context = {
        "request": request,
        "categories": await get_categories_index(),
        "user": None,
    }

    if request.scope["type"] == "websocket":
        cache_versions = await get_cache_versions()
        settings = await get_dynamic_settings(cache_versions)

        context.update(
            {
                "cache_versions": cache_versions,
                "settings": settings,
            }
        )
    else:
        context.update(
            {
                "cache_versions": request.state.cache_versions,
                "settings": request.state.settings,
            }
        )

    categories_loader.setup_context(context)
    categories_children_loader.setup_context(context)
    threads_loader.setup_context(context)
    posts_loader.setup_context(context)
    users_loader.setup_context(context)
    users_groups_loader.setup_context(context)

    return context


async def get_permissions(context: Context) -> dict:
    if context.get("user"):
        return await get_user_permissions(context, context["user"])
    return await get_anonymous_permissions(context)
