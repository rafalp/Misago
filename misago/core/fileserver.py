import os

from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse


SERVED_PATHS = (
    settings.MISAGO_ATTACHMENTS_ROOT,
    settings.MISAGO_AVATAR_CACHE,
)


def send_file(file_path, content_type, attachment=None):
    file_size = os.path.getsize(file_path)

    if settings.MISAGO_SENDFILE_HEADER:
        return send_header(file_path, content_type, file_size, attachment)
    else:
        return send_stream(file_path, content_type, file_size, attachment)


def send_header(file_path, content_type, file_size, attachment=None):
    if settings.MISAGO_SENDFILE_LOCATIONS_PATH:
        for path in SERVED_PATHS:
            if file_path.startswith(path):
                file_path = file_path[len(path):]
                file_path = '/%s' % settings.MISAGO_SENDFILE_LOCATIONS_PATH
                break

    response = HttpResponse()
    response[settings.MISAGO_SENDFILE_HEADER] = file_path
    del response['Content-Type']

    return response


def send_stream(file_path, content_type, file_size, attachment=None):
    response = StreamingHttpResponse(open(file_path, 'r'))

    response['Content-Type'] = content_type
    response['Content-Length'] = file_size
    if attachment:
        header = 'attachment; filename="%s"' % attachment
        response['Content-Disposition'] = header

    return response
