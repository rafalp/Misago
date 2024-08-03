from enum import Enum


class PluginOutlet(Enum):
    """Enum with standard plugin outlets defined by Misago.

    Members values are descriptions of outlets locations, used by the docs generator.
    """

    TEST = "Used in some tests."

    ADMIN_DASHBOARD_START = "On the admin dashboard page, above all other content."
    ADMIN_DASHBOARD_AFTER_CHECKS = "On the admin dashboard page, below the Checks card."
    ADMIN_DASHBOARD_AFTER_ANALYTICS = (
        "On the admin dashboard page, below the Analytics card."
    )
    ADMIN_DASHBOARD_END = "On the admin dashboard page, below all other content."

    LOGIN_PAGE_START = "On the sign in page, above the form."
    LOGIN_PAGE_END = "On the sign in page, below the form."

    CATEGORIES_LIST_START = "On the categories page, above the list."
    CATEGORIES_LIST_END = "On the categories page, below the list."

    THREADS_LIST_START = "On the threads page, above the list."
    THREADS_LIST_MIDDLE = "On the threads page, between the subcategories and the list."
    THREADS_LIST_END = "On the threads page, below the list."

    CATEGORY_THREADS_LIST_START = "On the category threads page, above the list."
    CATEGORY_THREADS_LIST_MIDDLE = (
        "On the category threads page, between the subcategories and the list."
    )
    CATEGORY_THREADS_LIST_END = "On the category threads page, below the list."

    PRIVATE_THREADS_LIST_START = "On the private threads page, above the list."
    PRIVATE_THREADS_LIST_END = "On the private threads page, below the list."

    THREADS_LIST_TOOLBAR_START = "On threads lists pages, at the start of the toolbar."
    THREADS_LIST_TOOLBAR_BEFORE_SPACER = (
        "On threads lists pages, before the toolbar's spacer."
    )
    THREADS_LIST_TOOLBAR_AFTER_SPACER = (
        "On threads lists pages, after the toolbar's spacer."
    )
    THREADS_LIST_TOOLBAR_END = "On threads lists pages, at the end of the toolbar."
