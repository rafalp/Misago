from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest, HttpResponse
from django.utils.translation import pgettext

from ...threads.models import Post
from ..redirect import redirect_to_post


def post(request: HttpRequest, post_id: int) -> HttpResponse:
    try:
        post_obj = Post.objects.get(id=post_id)
        return redirect_to_post(request, post_obj)
    except (PermissionDenied, Post.DoesNotExist) as error:
        # "Post not found" or permission error would leak post's existence
        raise Http404(pgettext("post not found error", "Thread not found")) from error
