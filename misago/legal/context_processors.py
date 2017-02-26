from django.urls import reverse

from misago.conf import settings


def legal_links(request):
    legal_context = {}

    if settings.terms_of_service_link:
        legal_context['TERMS_OF_SERVICE_URL'] = settings.terms_of_service_link
    elif settings.terms_of_service:
        legal_context['TERMS_OF_SERVICE_URL'] = reverse('misago:terms-of-service')

    if settings.privacy_policy_link:
        legal_context['PRIVACY_POLICY_URL'] = settings.privacy_policy_link
    elif settings.privacy_policy:
        legal_context['PRIVACY_POLICY_URL'] = reverse('misago:privacy-policy')

    if legal_context:
        request.frontend_context.update(legal_context)

    return legal_context
