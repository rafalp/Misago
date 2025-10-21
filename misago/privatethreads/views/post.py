from .generic import PrivateThreadView

from ...categories.enums import CategoryTree
from ...threads.redirect import redirect_to_post
from ...threads.views.post import PostLastView, PostUnreadView, PostView
from .generic import PrivateThreadView


class PrivateThreadPostLastView(PostLastView, PrivateThreadView):
    pass


class PrivateThreadPostUnreadView(PostUnreadView, PrivateThreadView):
    pass


class PrivateThreadPostView(PostView, PrivateThreadView):
    pass


redirect_to_post.view(CategoryTree.PRIVATE_THREADS, PrivateThreadPostView.as_view())
