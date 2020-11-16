import hashlib
from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.urls import resolve, reverse
from django.utils import html, timezone
from django.utils.encoding import force_text
from django.utils.module_loading import import_string

MISAGO_SLUGIFY = getattr(settings, "MISAGO_SLUGIFY", "misago.core.slugify.default")

slugify = import_string(MISAGO_SLUGIFY)


def format_plaintext_for_html(string):
    return html.linebreaks(html.urlize(html.escape(string)))


def encode_json_html(string):
    return string.replace("<", r"\u003C")


ISO8601_FORMATS = ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f")


def parse_iso8601_string(value):
    """turns ISO 8601 string into datetime object"""
    value = force_text(value, strings_only=True).rstrip("Z")

    for format_str in ISO8601_FORMATS:
        try:
            parsed_value = datetime.strptime(value, format_str)
            break
        except ValueError:
            try:
                parsed_value = datetime.strptime(value[:-6], format_str)
                break
            except ValueError:
                pass
    else:
        raise ValueError("failed to hydrate the %s timestamp" % value)

    offset_str = value[-6:]
    if offset_str and offset_str[0] in ("-", "+"):
        tz_offset = timedelta(hours=int(offset_str[1:3]), minutes=int(offset_str[4:6]))
        tz_offset = tz_offset.seconds // 60
        if offset_str[0] == "-":
            tz_offset *= -1
    else:
        tz_offset = 0

    tz_correction = timezone.get_fixed_timezone(tz_offset)
    return timezone.make_aware(parsed_value, tz_correction)


def hide_post_parameters(request):
    """
    Mark request as having sensitive parameters
    We can't use decorator because of DRF uses custom HttpRequest
    that is incompatibile with Django's decorator
    """
    request.sensitive_post_parameters = "__ALL__"


def clean_return_path(request):
    """return path utility that returns return path from referer or POST"""
    if request.method == "POST" and "return_path" in request.POST:
        return _get_return_path_from_post(request)
    return _get_return_path_from_referer(request)


def _get_return_path_from_post(request):
    return_path = request.POST.get("return_path")
    try:
        if not return_path:
            raise ValueError()
        if not return_path.startswith("/"):
            raise ValueError()
        resolve(return_path)
        return return_path
    except (Http404, ValueError):
        return None


def _get_return_path_from_referer(request):
    referer = request.META.get("HTTP_REFERER")
    try:
        if not referer:
            raise ValueError()
        if not referer.startswith(request.scheme):
            raise ValueError()
        referer = referer[len(request.scheme) + 3 :]
        if not referer.startswith(request.META["HTTP_HOST"]):
            raise ValueError()
        referer = referer[len(request.META["HTTP_HOST"].rstrip("/")) :]
        if not referer.startswith("/"):
            raise ValueError()
        resolve(referer)
        return referer
    except (Http404, KeyError, ValueError):
        return None


def is_request_to_misago(request):
    try:
        return request._request_to_misago
    except AttributeError:
        request._request_to_misago = _is_request_path_under_misago(request)
        return request._request_to_misago


def _is_request_path_under_misago(request):
    # We are assuming that forum_index link is root of all Misago links
    forum_index = reverse("misago:index")
    path = request.path

    if len(forum_index) > len(path):
        return False
    return path[: len(forum_index)] == forum_index


def is_referer_local(request):
    referer = request.META.get("HTTP_REFERER")

    if not referer:
        return False
    if not referer.startswith(request.scheme):
        return False
    referer = referer[len(request.scheme) + 3 :]
    if not referer.startswith(request.META["HTTP_HOST"]):
        return False
    referer = referer[len(request.META["HTTP_HOST"].rstrip("/")) :]
    if not referer.startswith("/"):
        return False

    return True


def get_exception_message(exception=None, default_message=None):
    if not exception:
        return default_message

    try:
        return exception.args[0]
    except IndexError:
        return default_message


def clean_ids_list(ids_list, error_message):
    try:
        return list(map(int, ids_list))
    except (ValueError, TypeError):
        raise PermissionDenied(error_message)


def get_host_from_address(address):
    if not address:
        return None

    if address.lower().startswith("https://"):
        address = address[8:]
    if address.lower().startswith("http://"):
        address = address[7:]

    address = address.lstrip("/")
    if "/" in address:
        address = address.split("/")[0] or address
    if ":" in address:
        address = address.split(":")[0] or address

    return address


HASH_LENGTH = 8


def get_file_hash(file_obj):
    if not file_obj.size:
        return "0" * HASH_LENGTH
    file_hash = hashlib.md5()
    for chunk in file_obj.chunks():
        file_hash.update(chunk)
    return file_hash.hexdigest()[:HASH_LENGTH]
