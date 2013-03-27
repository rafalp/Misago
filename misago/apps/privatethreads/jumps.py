from misago.apps.threadtype.jumps import *
from misago.apps.privatethreads.mixins import TypeMixin

class LastReplyView(LastReplyBaseView, TypeMixin):
    pass


class FindReplyView(FindReplyBaseView, TypeMixin):
    pass


class NewReplyView(NewReplyBaseView, TypeMixin):
    pass


class ShowHiddenRepliesView(ShowHiddenRepliesBaseView, TypeMixin):
    pass


class WatchThreadView(WatchThreadBaseView, TypeMixin):
    pass


class WatchEmailThreadView(WatchEmailThreadBaseView, TypeMixin):
    pass


class UnwatchThreadView(UnwatchThreadBaseView, TypeMixin):
    pass


class UnwatchEmailThreadView(UnwatchEmailThreadBaseView, TypeMixin):
    pass


class UpvotePostView(UpvotePostBaseView, TypeMixin):
    pass


class DownvotePostView(DownvotePostBaseView, TypeMixin):
    pass


class InviteUserView(JumpView, TypeMixin):
    def make_jump(self):
        print 'ZOMG INVITING USER'


class RemoveUserView(JumpView, TypeMixin):
    def make_jump(self):
        print 'ZOMG REMOVING USER'