from django.urls import reverse


def preload_threads_urls(request):
    request.frontend_context.update({
        'ATTACHMENTS_API': reverse('misago:api:attachment-list'),
        'THREAD_EDITOR_API': reverse('misago:api:thread-editor'),
        'THREADS_API': reverse('misago:api:thread-list'),
        'PRIVATE_THREADS_API': reverse('misago:api:private-thread-list'),
        'PRIVATE_THREADS_URL': reverse('misago:private-threads'),
    })

    return {}
