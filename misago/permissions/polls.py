from ..categories.models import Category
from ..polls.models import Poll
from ..threads.models import Thread
from .proxy import UserPermissionsProxy


def check_create_poll_permission(permissions: UserPermissionsProxy):
    pass


def check_create_poll_in_thread_permission(
    permissions: UserPermissionsProxy, category: Category, thread: Thread
):
    pass


def check_edit_poll_permission(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, poll: Poll
):
    pass


def check_delete_poll_permission(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, poll: Poll
):
    pass


def check_close_poll_permission(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, poll: Poll
):
    pass


def check_vote_in_poll_permission(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, poll: Poll
):
    pass
