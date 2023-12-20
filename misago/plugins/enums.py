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
    CATEGORIES_LIST_START = "On the categories page, above the list."
    CATEGORIES_LIST_END = "On the categories page, under the list."
