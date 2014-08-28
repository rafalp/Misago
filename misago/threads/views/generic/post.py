from misago.threads.views.generic.base import ViewBase


__all__ = ['PostView']


class PostView(ViewBase):
    """
    Basic view for posts
    """
    def fetch_post(self, request, **kwargs):
        pass

    def dispatch(self, request, *args, **kwargs):
        post = self.fetch_post(request, **kwargs)
