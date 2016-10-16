import os

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from ..models import Attachment, AttachmentType


ATTACHMENT_404_URL = '/'.join((settings.STATIC_URL, settings.MISAGO_404_IMAGE))
ATTACHMENT_403_URL = '/'.join((settings.STATIC_URL, settings.MISAGO_403_IMAGE))


def attachment_server(request, pk, secret, thumbnail=False):
    try:
        url = serve_file(request, pk, secret, thumbnail)
        return redirect(url)
    except Http404:
        return redirect(ATTACHMENT_404_URL)
    except PermissionDenied:
        return redirect(ATTACHMENT_403_URL)


def serve_file(request, pk, secret, thumbnail):
    queryset = Attachment.objects.select_related('filetype')
    attachment = get_object_or_404(queryset, pk=pk, secret=secret)

    if not request.user.is_staff:
        allow_file_download(request, attachment)

    attachment.downloads = F('downloads') + 1
    attachment.save(update_fields=['downloads'])

    if attachment.is_image:
        if thumbnail:
            return attachment.thumbnail.url
        else:
            return attachment.image.url
    else:
        if thumbnail:
            raise Http404()
        else:
            return attachment.file.url


def allow_file_download(request, attachment):
    is_authenticated = request.user.is_authenticated()

    if not attachment.post_id or not request.user.acl['can_download_other_users_attachments']:
        if not is_authenticated or request.user.id != attachment.uploader_id:
            raise PermissionDenied()

    allowed_roles = set(r.pk for r in attachment.filetype.limit_downloaders_to.all())
    if allowed_roles:
        user_roles = set(r.pk for r in request.user.get_roles())
        if not user_roles & allowed_roles:
            raise PermissionDenied()

    if attachment.filetype.status == AttachmentType.DISABLED:
        raise PermissionDenied()
