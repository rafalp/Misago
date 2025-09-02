from django.db.models import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.views import View

from ..categories.enums import CategoryTree
from ..threads.models import Post, Thread
from ..threads.views.generic import PrivateThreadView
from ..threads.views.redirect import RedirectView, redirect_to_thread_post
from .hooks import redirect_to_post_hook


class PostRedirectView(View):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        return self.real_dispatch(request, id)

    def post(self, request: HttpRequest, id: int) -> HttpResponse:
        return self.real_dispatch(request, id)

    def real_dispatch(self, request: HttpRequest, id: int) -> HttpResponse:
        try:
            post = Post.objects.select_related("category").get(id=id)
        except Post.DoesNotExist:
            raise Http404()

        return redirect_to_post(request, post)


def redirect_to_post(request: Http404, post: Post) -> HttpResponse:
    return redirect_to_post_hook(
        _redirect_to_post_action, request, post
    )


def _redirect_to_post_action(request: Http404, post: Post) -> HttpResponse:
    if post.category.tree_id == CategoryTree.THREADS:
        return redirect_to_thread_post(request, post.thread_id, "", post=post.id)

    if post.category.tree_id == CategoryTree.PRIVATE_THREADS:
        return redirect_to_private_thread_post(request, post.thread_id, "", post=post.id)

    raise Http404()


class RedirectToPost(RedirectView):
    def get_post(
        self, request: HttpRequest, thread: Thread, queryset: QuerySet, kwargs: dict
    ) -> Post | None:
        try:
            return queryset.get(id=kwargs["post"])
        except Post.DoesNotExist:
            raise Http404()


class PrivateThreadRedirectToPost(RedirectToPost, PrivateThreadView):
    pass


redirect_to_private_thread_post = PrivateThreadRedirectToPost.as_view()
