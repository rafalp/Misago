from django.http import StreamingHttpResponse
from django.template import RequestContext
from misago.apps.errors import error403, error404
from misago.models import Attachment
from misago.readstrackers import ForumsTracker
from misago.shortcuts import render_to_response

def server(self, attachment, thumb=False):
    try:
        attachment = Attachment.objects.select_related('forum', 'thread', 'user').get(hash_id=attachment)
        if thumb:
            response = StreamingHttpResponse(open(attachment.thumb_path), content_type=attachment.content_type)
        else:
            response = StreamingHttpResponse(open(attachment.file_path), content_type=attachment.content_type)
            response['Cache-Control'] = 'no-cache'
        if not attachment.is_image:
            response['Content-Disposition'] = 'attachment;filename="%s"' % attachment.name
        return response
    except Attachment.DoesNotExist:
        pass