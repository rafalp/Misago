from enum import Enum


class PluginOutlet(Enum):
    """Enum with standard plugin outlets defined by Misago.

    Members values are descriptions of outlets locations, used by the docs generator.
    """

    ADMIN_DASHBOARD_START = "On the Admin dashboard page, above all other content."
    ADMIN_DASHBOARD_AFTER_CHECKS = "On the Admin dashboard page, below the Checks card."
    ADMIN_DASHBOARD_AFTER_ANALYTICS = (
        "On the Admin dashboard page, below the Analytics card."
    )
    ADMIN_DASHBOARD_END = "On the Admin dashboard page, below all other content."

    ATTACHMENT_PAGE_START = "On the attachment details page, above the preview."
    ATTACHMENT_PAGE_AFTER_PREVIEW = "On the attachment details page, under the preview."
    ATTACHMENT_PAGE_END = "On the attachment details page, under the details block."

    ATTACHMENT_DELETE_PAGE_START = (
        "On the attachment delete page, above the confirmation block."
    )
    ATTACHMENT_DELETE_PAGE_END = (
        "On the attachment delete page, below the confirmation block."
    )

    LOGIN_PAGE_START = "On the Sign in page, above the form."
    LOGIN_PAGE_END = "On the Sign in page, below the form."

    CATEGORIES_LIST_START = "On the Categories page, above the list."
    CATEGORIES_LIST_END = "On the Categories page, below the list."

    THREADS_LIST_START = "On the Threads page, above the list."
    THREADS_LIST_MIDDLE = "On the Threads page, between the subcategories and the list."
    THREADS_LIST_END = "On the Threads page, below the list."

    CATEGORY_THREADS_LIST_START = "On the Category threads page, above the list."
    CATEGORY_THREADS_LIST_MIDDLE = (
        "On the Category threads page, between the subcategories and the list."
    )
    CATEGORY_THREADS_LIST_END = "On the Category threads page, below the list."

    PRIVATE_THREADS_LIST_START = "On the Private threads page, above the list."
    PRIVATE_THREADS_LIST_END = "On the Private threads page, below the list."

    THREADS_LIST_TOOLBAR_START = "On threads lists pages, at the start of the toolbar."
    THREADS_LIST_TOOLBAR_BEFORE_SPACER = (
        "On threads lists pages, before the toolbar's spacer."
    )
    THREADS_LIST_TOOLBAR_AFTER_SPACER = (
        "On threads lists pages, after the toolbar's spacer."
    )
    THREADS_LIST_TOOLBAR_END = "On threads lists pages, at the end of the toolbar."

    THREAD_REPLIES_PAGE_START = "On the Thread replies page, below the page's header."
    THREAD_REPLIES_PAGE_END = (
        "On the Thread replies page, above the bottom breadcrumbs."
    )

    THREAD_REPLIES_PAGE_TOOLBAR_START = (
        "On the Thread replies page, at the start of the toolbar."
    )
    THREAD_REPLIES_PAGE_TOOLBAR_BEFORE_SPACER = (
        "On the Thread replies page, before the toolbar's spacer."
    )
    THREAD_REPLIES_PAGE_TOOLBAR_AFTER_SPACER = (
        "On the Thread replies page, after the toolbar's spacer."
    )
    THREAD_REPLIES_PAGE_TOOLBAR_END = (
        "On the Thread replies page, at the end of the toolbar."
    )

    PRIVATE_THREAD_REPLIES_PAGE_START = (
        "On the Private thread replies page, below the page's header."
    )
    PRIVATE_THREAD_REPLIES_PAGE_END = (
        "On the Private thread replies page, above the bottom breadcrumbs."
    )

    PRIVATE_THREAD_REPLIES_PAGE_TOOLBAR_START = (
        "On the Private thread replies page, at the start of the toolbar."
    )
    PRIVATE_THREAD_REPLIES_PAGE_TOOLBAR_BEFORE_SPACER = (
        "On the Private thread replies page, before the toolbar's spacer."
    )
    PRIVATE_THREAD_REPLIES_PAGE_TOOLBAR_AFTER_SPACER = (
        "On the Private thread replies page, after the toolbar's spacer."
    )
    PRIVATE_THREAD_REPLIES_PAGE_TOOLBAR_END = (
        "On the Private thread replies page, at the end of the toolbar."
    )

    MARKUP_EDITOR_TOOLBAR_START = "At the start of the markup editor's toolbar."
    MARKUP_EDITOR_TOOLBAR_BEFORE_RULER = "On the the markup editor's toolbar, between strikethrough and insert horizontal."
    MARKUP_EDITOR_TOOLBAR_BEFORE_LINK = "On the the markup editor's toolbar, between insert horizontal ruler and insert link."
    MARKUP_EDITOR_TOOLBAR_BEFORE_QUOTE = (
        "On the the markup editor's toolbar, between insert photo and insert quote."
    )
    MARKUP_EDITOR_TOOLBAR_END = "At the end of the markup editor's toolbar."

    TEST = "Used in some tests."
