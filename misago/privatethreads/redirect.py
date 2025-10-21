from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from ..permissions.privatethreads import filter_private_thread_posts_queryset
from ..threads.models import Post, Thread
from ..threads.paginator import ThreadPostsPaginator


def redirect_to_private_thread_post(
    request: HttpRequest, thread: Thread, post: Post
) -> HttpResponse:
    queryset = filter_private_thread_posts_queryset(
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

    url = reverse("misago:private-thread", kwargs=url_kwargs) + f"#post-{post.id}"

    return redirect(url)
