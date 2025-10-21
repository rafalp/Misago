from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from ..categories.treeid import get_category_tree_id
from ..permissions.threads import filter_thread_posts_queryset
from .models import Post, Thread
from .paginator import ThreadPostsPaginator


class PostRedirectView:
    def __call__(
        self, request: HttpRequest, *, id: int, slug: str, post_id: int
    ) -> HttpResponse: ...


class PostRedirectRouter:
    views: dict[int, PostRedirectView]

    def __init__(self):
        self.views = {}

    def view(self, tree_id: int, view: PostRedirectView):
        self.views[tree_id] = view

    def __call__(self, request: HttpRequest, post: Post) -> HttpResponse:
        tree_id = get_category_tree_id(post.category_id)

        try:
            view = self.views[tree_id]
        except KeyError as error:
            raise ValueError(f"Unknown 'Category' type: {tree_id}") from error

        return view(request, thread_id=post.thread_id, slug="", post_id=post.id)


redirect_to_post = PostRedirectRouter()


def redirect_to_thread_post(
    request: HttpRequest, thread: Thread, post: Post
) -> HttpResponse:
    queryset = filter_thread_posts_queryset(
        request.user_permissions, thread, thread.post_set.order_by("id")
    )
    paginator = ThreadPostsPaginator(
        queryset,
        request.settings.posts_per_page,
        request.settings.posts_per_page_orphans,
    )

    offset = queryset.filter(id__lt=post.id).count()
    page = paginator.get_item_page(offset)

    url_kwargs = {"thread_id": thread.id, "slug": thread.slug}
    if page > 1:
        url_kwargs["page"] = page

    url = reverse("misago:thread", kwargs=url_kwargs) + f"#post-{post.id}"

    return redirect(url)
