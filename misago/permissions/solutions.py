from ..threads.models import Post, Thread
from .hooks import (
    check_clear_thread_solution_permission_hook,
    check_select_thread_solution_permission_hook,
)
from .proxy import UserPermissionsProxy


def check_select_thread_solution_permission(
    permissions: UserPermissionsProxy, post: Post
):
    check_select_thread_solution_permission_hook(
        _check_select_thread_solution_permission_action,
        permissions,
        post,
    )


def _check_select_thread_solution_permission_action(
    permissions: UserPermissionsProxy, post: Post
):
    if not permissions.user.is_authenticated:
        pass

    # MOD OR OP
    # CATEGORY/THREAD CLOSED
    # POST PROTECTED
    # IF THREAD HAS SOLUTION, CHECK IF TIME FOR A CHANGE


def check_clear_thread_solution_permission(
    permissions: UserPermissionsProxy, thread: Thread
):
    check_clear_thread_solution_permission_hook(
        _check_clear_thread_solution_permission_action,
        permissions,
        thread,
    )


def _check_clear_thread_solution_permission_action(
    permissions: UserPermissionsProxy, thread: Thread
):
    # AUTHENTICATED
    if not permissions.user.is_authenticated:
        pass

    # MOD OR OP

    # CATEGORY/THREAD CLOSED

    # POST PROTECTED

    # CHECK IF TIME FOR A CHANGE
