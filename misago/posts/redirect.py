from django.http import HttpRequest, HttpResponse

from ..categories.treeid import get_category_tree_id
from .models import Post


class RedirectView:
    def __call__(
        self, request: HttpRequest, *, thread_id: int, slug: str, post: int
    ) -> HttpResponse: ...


class PostRedirect:
    views: dict[int, RedirectView]

    def __init__(self):
        self.views = {}

    def view(self, tree_id: int, view: RedirectView):
        self.views[tree_id] = view

    def __call__(self, request: HttpRequest, post: Post) -> HttpResponse:
        tree_id = get_category_tree_id(post.category_id)

        try:
            view = self.views[tree_id]
        except KeyError as error:
            raise ValueError(f"Unknown 'Category' type: {tree_id}") from error

        return view(request, id=post.thread_id, slug="", post=post.id)


redirect_to_post = PostRedirect()
