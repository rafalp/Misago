from misago.apps.threadtype.delete import *
from misago.apps.privatethreads.mixins import TypeMixin

class DeleteThreadView(DeleteThreadBaseView, TypeMixin):
    pass


class HideThreadView(HideThreadBaseView, TypeMixin):
    pass


class ShowThreadView(ShowThreadBaseView, TypeMixin):
    pass


class DeleteReplyView(DeleteReplyBaseView, TypeMixin):
    pass


class HideReplyView(HideReplyBaseView, TypeMixin):
    pass


class ShowReplyView(ShowReplyBaseView, TypeMixin):
    pass


class DeleteCheckpointView(DeleteCheckpointBaseView, TypeMixin):
    pass


class HideCheckpointView(HideCheckpointBaseView, TypeMixin):
    pass


class ShowCheckpointView(ShowCheckpointBaseView, TypeMixin):
    pass