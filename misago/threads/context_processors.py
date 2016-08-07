from django.core.urlresolvers import reverse


def preload_threads_urls(request):
    request.frontend_context.update({
        'THREAD_EDITOR_URL': reverse('misago:api:thread-editor')
    })

    return {}
