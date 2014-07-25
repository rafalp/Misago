import os

from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse


SERVED_PATHS = (
    settings.MISAGO_ATTACHMENTS_ROOT,
    settings.MISAGO_AVATAR_STORE,
)


def make_file_response(file_path, content_type, attachment=None):
    file_size = os.path.getsize(file_path)

    response_args = (file_path, content_type, file_size, attachment)
    if settings.MISAGO_SENDFILE_HEADER:
        return make_header_response(*response_args)
    else:
        return make_stream_response(*response_args)


def make_header_response(file_path, content_type, file_size, attachment=None):
    if settings.MISAGO_SENDFILE_LOCATIONS_PATH:
        file_path = rewrite_file_path(file_path)

    response = HttpResponse()
    response[settings.MISAGO_SENDFILE_HEADER] = file_path
    del response['Content-Type']

    return response


def rewrite_file_path(file_path):
    for path in SERVED_PATHS:
        if file_path.startswith(path):
            suffix = file_path[len(path):]
            return '/%s%s' % (settings.MISAGO_SENDFILE_LOCATIONS_PATH, suffix)
    else:
        raise ValueError("'%s' path is not supported" % file_path)


def make_stream_response(file_path, content_type, file_size, attachment=None):
    response = StreamingHttpResponse(open(file_path, 'r'))

    response['Content-Type'] = content_type
    response['Content-Length'] = file_size
    if attachment:
        header = 'attachment; filename="%s"' % attachment
        response['Content-Disposition'] = header

    return response
