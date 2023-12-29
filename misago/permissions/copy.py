from django.http import HttpRequest

from ..users.models import Group
from .hooks import copy_group_permissions_hook

__all__ = ["copy_group_permissions"]


def copy_group_permissions(
    src: Group,
    dst: Group,
    request: HttpRequest | None = None,
) -> None:
    copy_group_permissions_hook(_copy_group_permissions_action, src, dst, request)


def _copy_group_permissions_action(
    src: Group,
    dst: Group,
    request: HttpRequest | None = None,
) -> None:
    pass
