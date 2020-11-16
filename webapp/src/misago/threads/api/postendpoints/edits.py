from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.response import Response

from ....acl.objectacl import add_acl_to_obj
from ....core.shortcuts import get_int_or_404
from ....markup import common_flavour
from ....users.online.utils import make_users_status_aware
from ...checksums import update_post_checksum
from ...serializers import PostEditSerializer, PostSerializer


def get_edit_endpoint(request, post):
    edit = get_edit(post, request.GET.get("edit"))

    data = PostEditSerializer(edit).data

    try:
        queryset = post.edits_record.filter(id__gt=edit.id).order_by("id")
        data["next"] = queryset[:1][0].id
    except IndexError:
        data["next"] = None

    try:
        queryset = post.edits_record.filter(id__lt=edit.id).order_by("-id")
        data["previous"] = queryset[:1][0].id
    except IndexError:
        data["previous"] = None

    return Response(data)


def revert_post_endpoint(request, post):
    edit = get_edit_by_pk(post, request.GET.get("edit"))

    datetime = timezone.now()
    post_edits = post.edits

    post.edits_record.create(
        category=post.category,
        thread=post.thread,
        edited_on=datetime,
        editor=request.user,
        editor_name=request.user.username,
        editor_slug=request.user.slug,
        edited_from=post.original,
        edited_to=edit.edited_from,
    )

    parsing_result = common_flavour(request, post.poster, edit.edited_from)

    post.original = parsing_result["original_text"]
    post.parsed = parsing_result["parsed_text"]

    update_post_checksum(post)

    post.updated_on = datetime
    post.edits = F("edits") + 1

    post.last_editor = request.user
    post.last_editor_name = request.user.username
    post.last_editor_slug = request.user.slug

    post.save()

    post.is_read = True
    post.is_new = False
    post.edits = post_edits + 1

    add_acl_to_obj(request.user_acl, post)

    if post.poster:
        make_users_status_aware(request, [post.poster])

    return Response(PostSerializer(post, context={"user": request.user}).data)


def get_edit(post, pk=None):
    if pk is not None:
        return get_edit_by_pk(post, pk)

    edit = post.edits_record.first()
    if not edit:
        raise PermissionDenied(_("Edits record is unavailable for this post."))
    return edit


def get_edit_by_pk(post, pk):
    return get_object_or_404(post.edits_record, pk=get_int_or_404(pk))
