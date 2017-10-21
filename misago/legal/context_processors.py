from django.urls import reverse

from misago.conf import settings


def legal_links(request):
    if settings.terms_of_service_link:
        request.frontend_context['url'].update({
            'tos': settings.terms_of_service_link,
        })
    elif settings.terms_of_service:
        request.frontend_context['url'].update({
            'tos': reverse('misago:terms-of-service'),
        })

    if settings.privacy_policy_link:
        request.frontend_context['url'].update({
            'privacy_policy': settings.privacy_policy_link,
        })
    elif settings.privacy_policy:
        request.frontend_context['url'].update({
            'privacy_policy': reverse('misago:privacy-policy'),
        })

    return {}
