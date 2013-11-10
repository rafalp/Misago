from django.conf import settings
from django.http import StreamingHttpResponse
from django.template import RequestContext
from misago.acl.exceptions import ACLError403, ACLError404
from django.utils.translation import ugettext as _
from misago.apps.errors import error403, error404
from misago.models import Attachment
from misago.readstrackers import ForumsTracker
from misago.shortcuts import render_to_response

def server(request, attachment, thumb=False):
    try:
        attachment = Attachment.objects.select_related('forum', 'thread', 'post', 'user').get(hash_id=attachment)
        request.acl.forums.allow_forum_view(attachment.forum)
        if attachment.thread:
            request.acl.threads.allow_thread_view(request.user, attachment.thread)
            if attachment.forum.special == 'private_threads':
                if not request.user.is_authenticated():
                    raise ACLError404()
                can_see_thread_because_reported = (
                    request.acl.privatethreads.is_mod() and attachment.thread.replies_reported)
                can_see_thread_because_participates = request.user in thread.participants
                if not (can_see_thread_because_reported or can_see_thread_because_participates):
                    raise ACLError404()
            if attachment.post:
                request.acl.threads.allow_post_view(request.user, attachment.thread, attachment.post)
                request.acl.threads.allow_attachment_download(request.user, attachment.forum, attachment.post)
        return serve_file(attachment, thumb)
    except ACLError403:
        if attachment.is_image:
            return serve_403_image()
        return error403(request,  _("You don't have permission to download this file."))
    except (Attachment.DoesNotExist, ACLError404):
        if thumb:
            return serve_404_image()
        return error404(request, _("Requested file could not be found."))


def serve_file(attachment, thumb):
    if thumb:
        response = StreamingHttpResponse(open(attachment.thumb_path), content_type=attachment.content_type)
    else:
        response = StreamingHttpResponse(open(attachment.file_path), content_type=attachment.content_type)
        response['Cache-Control'] = 'no-cache'
    if not attachment.is_image:
        response['Content-Disposition'] = 'attachment;filename="%s"' % attachment.name
    return response


def serve_403_image():
    response = StreamingHttpResponse(open('%s403.png' % settings.ATTACHMENTS_ROOT), content_type='image/png')
    response['Cache-Control'] = 'no-cache'
    return response


def serve_404_image():
    response = StreamingHttpResponse(open('%s404.png' % settings.ATTACHMENTS_ROOT), content_type='image/png')
    response['Cache-Control'] = 'no-cache'
    return response