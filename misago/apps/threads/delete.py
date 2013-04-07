from misago.apps.threadtype.delete import *
from misago.apps.threads.mixins import TypeMixin

class DeleteThreadView(DeleteThreadBaseView, TypeMixin):
    pass


class HideThreadView(HideThreadBaseView, TypeMixin):
    pass


class DeleteReplyView(DeleteReplyBaseView, TypeMixin):
    pass


class HideReplyView(HideReplyBaseView, TypeMixin):
    pass


class DeleteCheckpointView(DeleteCheckpointBaseView, TypeMixin):
    pass


class HideCheckpointView(HideCheckpointBaseView, TypeMixin):
    pass


class ShowCheckpointView(ShowCheckpointBaseView, TypeMixin):
    pass