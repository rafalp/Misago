from django.db.transaction import atomic
from django.http import JsonResponse

from misago.threads.views.generic.base import ViewBase


__all__ = ['QuotePostView']


class PostView(ViewBase):
    is_atomic = True

    def dispatch(self, request, *args, **kwargs):
        if self.is_atomic:
            with atomic():
                post = self.get_post(request, True, **kwargs)
                return self.real_dispatch(request, post)
        else:
            post = self.get_post(request, **kwargs)
            return self.real_dispatch(request, post)

    def real_dispatch(self, request, post):
        raise NotImplementedError(
            "post views have to override real_dispatch method")


class QuotePostView(PostView):
    def real_dispatch(self, request, post):
        quote_tpl = u'[quote="%s, post:%s, topic:%s"]\n%s\n[/quote]'
        formats = (post.poster_name, post.pk, post.thread_id, post.original)
        return JsonResponse({
            'quote': quote_tpl % formats
        })
