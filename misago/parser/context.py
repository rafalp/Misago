from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest

from ..conf.dynamicsettings import DynamicSettings
from ..permissions.proxy import UserPermissionsProxy
from .forumaddress import ForumAddress
from .hooks import create_parser_context_hook

User = get_user_model()


@dataclass(frozen=True)
class ParserContext:
    content_type: str | None
    forum_address: ForumAddress
    request: HttpRequest | None
    user_permissions: UserPermissionsProxy
    user: User | AnonymousUser
    settings: DynamicSettings
    cache_versions: dict
    plugin_data: dict


def create_parser_context(
    *,
    request: HttpRequest | None = None,
    user_permissions: UserPermissionsProxy,
    settings: DynamicSettings,
    cache_versions: dict,
    content_type: str | None = None,
) -> ParserContext:
    return create_parser_context_hook(
        _create_parser_context_action,
        request=request,
        user_permissions=user_permissions,
        settings=settings,
        cache_versions=cache_versions,
        content_type=content_type,
    )


def _create_parser_context_action(
    *,
    request: HttpRequest | None,
    user_permissions: UserPermissionsProxy,
    settings: dict,
    cache_versions: dict,
    content_type: str | None,
) -> ParserContext:
    data = {
        "user_permissions": None,
        "user": None,
        "settings": None,
        "cache_versions": None,
        "plugin_data": {},
    }

    if user_permissions:
        data["user_permissions"] = user_permissions
        data["user"] = user_permissions.user

    if settings:
        data["settings"] = settings
    elif request:
        data["settings"] = request.settings
    else:
        raise ValueError("'settings' argument is required")

    if cache_versions:
        data["cache_versions"] = cache_versions
    elif request:
        data["cache_versions"] = request.cache_versions
    else:
        raise ValueError("'cache_versions' argument is required")

    return ParserContext(
        content_type=content_type,
        forum_address=DynamicSettings(data["settings"]),
        request=request,
        **data,
    )
