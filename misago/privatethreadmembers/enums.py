from enum import StrEnum


class PrivateThreadMembersTemplate(StrEnum):
    ADD = "misago/private_thread_members/add.html"
    ADD_MODAL = "misago/private_thread_members/add_modal.html"
    ADD_HTMX = "misago/private_thread_members/add_htmx.html"
    HTMX = "misago/private_thread_members/htmx.html"
    LIST = "misago/private_thread_members/list.html"
    MEMBER_REMOVE = "misago/private_thread_members/member_remove.html"
    OWNER_CHANGE = "misago/private_thread_members/owner_change.html"
