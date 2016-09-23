from django.core.urlresolvers import reverse


def preload_api_url(request):
    request.frontend_context.update({
        'PARSE_MARKUP_API': reverse('misago:api:parse-markup')
    })

    return {}
