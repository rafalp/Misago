from typing import Awaitable, Protocol

from ...context import Context
from ...hooks import FilterHook


class GetGroupsPermissionsAction(Protocol):
    async def __call__(
        self,
        context: Context,
        state: dict,
        groups_permissions: dict,
        *,
        anonymous: bool = False,
    ) -> dict:
        pass


class GetGroupsPermissionsFilter(Protocol):
    async def __call__(
        self,
        action: GetGroupsPermissionsAction,
        context: Context,
        state: dict,
        groups_permissions: dict,
        *,
        anonymous: bool = False,
    ) -> dict:
        pass


class GetGroupsPermissionsHook(
    FilterHook[GetGroupsPermissionsAction, GetGroupsPermissionsFilter]
):
    def call_action(
        self,
        action: GetGroupsPermissionsAction,
        context: Context,
        state: dict,
        groups_permissions: dict,
        *,
        anonymous: bool = False,
    ) -> Awaitable[dict]:
        return self.filter(
            action,
            context,
            state,
            groups_permissions,
            anonymous=anonymous,
        )


get_groups_permissions_hook = GetGroupsPermissionsHook()
