from misago.apps.threadtype.delete import *
from misago.apps.privatethreads.mixins import TypeMixin

class DeleteThreadView(DeleteThreadBaseView, TypeMixin):
    pass


class HideThreadView(HideThreadBaseView, TypeMixin):
    pass


class DeleteReplyView(DeleteReplyBaseView, TypeMixin):
    pass


class HideReplyView(HideReplyBaseView, TypeMixin):
    pass