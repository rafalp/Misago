from ariadne_graphql_modules import CollectionType

from .queries import AdminSettingsQueries, SettingsQueries
from .settings import AdminSettingsType, SettingsType
from .settingsupdate import AdminSettingsUpdateMutation


class AdminSettingsMutations(CollectionType):
    __types__ = [
        AdminSettingsUpdateMutation,
    ]


__all__ = [
    "AdminSettingsMutations",
    "AdminSettingsQueries",
    "AdminSettingsType",
    "SettingsQueries",
    "SettingsType",
]
