from django.urls import reverse

from misago.conf import settings


def legal_links(request):
    if settings.privacy_policy_link:
        request.frontend_context['url'].update({
            'privacy_policy': settings.privacy_policy_link,
        })
    elif settings.privacy_policy:
        request.frontend_context['url'].update({
            'privacy_policy': reverse('misago:privacy-policy'),
        })

    if settings.terms_of_service_link:
        request.frontend_context['url'].update({
            'tos': settings.terms_of_service_link,
        })
    elif settings.terms_of_service:
        request.frontend_context['url'].update({
            'tos': reverse('misago:terms-of-service'),
        })

    return {
        'privacy_policy': settings.privacy_policy_link or settings.privacy_policy,
        'terms_of_service': settings.terms_of_service_link or settings.terms_of_service,
    }
