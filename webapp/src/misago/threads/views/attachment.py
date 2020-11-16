from django.templatetags.static import static
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from ...conf import settings
from ..models import Attachment, AttachmentType


def attachment_server(request, pk, secret, thumbnail=False):
    try:
        url = serve_file(request, pk, secret, thumbnail)
        return redirect(url)
    except PermissionDenied:
        error_image = request.settings.attachment_403_image
        if not error_image:
            error_image = static(settings.MISAGO_ATTACHMENT_403_IMAGE)
        return redirect(error_image)
    except Http404:
        error_image = request.settings.attachment_404_image
        if not error_image:
            error_image = static(settings.MISAGO_ATTACHMENT_404_IMAGE)
        return redirect(error_image)


def serve_file(request, pk, secret, thumbnail):
    queryset = Attachment.objects.select_related("filetype")
    attachment = get_object_or_404(queryset, pk=pk, secret=secret)

    if not attachment.post_id and request.GET.get("shva") != "1":
        # if attachment is orphaned, don't run acl test unless explicitly told so
        # this saves user suprise of deleted attachment still showing in posts/quotes
        raise Http404()

    if not request.user.is_staff:
        allow_file_download(request, attachment)

    if attachment.is_image:
        if thumbnail and attachment.thumbnail:
            return attachment.thumbnail.url
        return attachment.image.url

    if thumbnail:
        raise Http404()
    return attachment.file.url


def allow_file_download(request, attachment):
    is_authenticated = request.user.is_authenticated

    if not is_authenticated or request.user.id != attachment.uploader_id:
        if not attachment.post_id:
            raise Http404()
        if not request.user_acl["can_download_other_users_attachments"]:
            raise PermissionDenied()

    allowed_roles = set(r.pk for r in attachment.filetype.limit_downloads_to.all())
    if allowed_roles:
        user_roles = set(r.pk for r in request.user.get_roles())
        if not user_roles & allowed_roles:
            raise PermissionDenied()

    if attachment.filetype.status == AttachmentType.DISABLED:
        raise PermissionDenied()
