from misago.apps.threadtype.changelog import (ChangelogChangesBaseView,
                                              ChangelogDiffBaseView,
                                              ChangelogRevertBaseView)
from misago.apps.threads.mixins import TypeMixin

class ChangelogView(ChangelogChangesBaseView, TypeMixin):
    pass


class ChangelogDiffView(ChangelogDiffBaseView, TypeMixin):
    pass


class ChangelogRevertView(ChangelogRevertBaseView, TypeMixin):
    pass