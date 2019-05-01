from django.utils.translation import get_language

from .. import __version__
from .momentjs import get_locale_url


def misago_version(request):
    return {"MISAGO_VERSION": __version__}


def site_address(request):
    if request.is_secure():
        site_protocol = "https"
        address_template = "https://%s"
    else:
        site_protocol = "http"
        address_template = "http://%s"

    host = request.get_host()

    return {
        "SITE_PROTOCOL": site_protocol,
        "SITE_HOST": host,
        "SITE_ADDRESS": address_template % host,
        "REQUEST_PATH": request.path,
    }


def current_link(request):
    if not request.resolver_match or request.frontend_context.get("CURRENT_LINK"):
        return {}

    url_name = request.resolver_match.url_name
    if request.resolver_match.namespaces:
        namespaces = ":".join(request.resolver_match.namespaces)
        link_name = "%s:%s" % (namespaces, url_name)
    else:
        link_name = url_name

    request.frontend_context.update({"CURRENT_LINK": link_name})

    return {}


def momentjs_locale(request):
    return {"MOMENTJS_LOCALE_URL": get_locale_url(get_language())}


def frontend_context(request):
    if request.include_frontend_context:
        return {"frontend_context": request.frontend_context}
    return {}
