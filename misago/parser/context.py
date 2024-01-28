from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest

from ..conf.dynamicsettings import DynamicSettings
from ..permissions.proxy import UserPermissionsProxy
from .forumaddress import ForumAddress
from .hooks import setup_parser_context_hook

User = get_user_model()


@dataclass(frozen=True)
class ParserContext:
    content_type: str | None
    forum_address: ForumAddress
    request: HttpRequest | None
    user: User | AnonymousUser
    user_permissions: UserPermissionsProxy
    cache_versions: dict
    settings: DynamicSettings
    plugin_data: dict


def create_parser_context(
    request: HttpRequest | None = None,
    *,
    user_permissions: UserPermissionsProxy | None = None,
    cache_versions: dict | None = None,
    settings: DynamicSettings | None = None,
    content_type: str | None = None,
) -> ParserContext:
    data = {
        "user_permissions": None,
        "user": None,
        "cache_versions": None,
        "settings": None,
        "plugin_data": {},
    }

    if user_permissions:
        data["user"] = user_permissions.user
        data["user_permissions"] = user_permissions
    elif request:
        data["user"] = request.user
        data["user_permissions"] = request.user_permissions
    else:
        raise TypeError(
            "'user_permissions' argument is required if 'request' is not set"
        )

    if cache_versions:
        data["cache_versions"] = cache_versions
    elif request:
        data["cache_versions"] = request.cache_versions
    else:
        raise TypeError("'cache_versions' argument is required if 'request' is not set")

    if settings:
        data["settings"] = settings
    elif request:
        data["settings"] = request.settings
    else:
        raise TypeError("'settings' argument is required if 'request' is not set")

    context = ParserContext(
        content_type=content_type,
        forum_address=ForumAddress(data["settings"]),
        request=request,
        **data,
    )

    if not setup_parser_context_hook:
        return context

    return setup_parser_context_hook(_context_lambda, context)


_context_lambda = lambda c: c
