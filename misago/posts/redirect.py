from django.http import HttpRequest, HttpResponse

from ..categories.treeid import get_category_tree_id
from .models import Post


class PostRedirectView:
    def __call__(
        self, request: HttpRequest, *, id: int, slug: str, post_id: int
    ) -> HttpResponse: ...


class PostRedirect:
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

        return view(request, id=post.thread_id, slug="", post_id=post.id)


redirect_to_post = PostRedirect()
