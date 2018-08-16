from django.urls import reverse

from .models import Agreement


def legal_links(request):
    agreements = Agreement.objects.get_agreements()

    legal_context = {}

    terms_of_service = agreements.get(Agreement.TYPE_TOS)
    if terms_of_service:
        if terms_of_service['link']:
            legal_context['TERMS_OF_SERVICE_URL'] = terms_of_service['link']
        elif terms_of_service['text']:
            legal_context['TERMS_OF_SERVICE_URL'] = reverse('misago:terms-of-service')

    privacy_policy = agreements.get(Agreement.TYPE_PRIVACY)
    if privacy_policy:
        if privacy_policy['link']:
            legal_context['PRIVACY_POLICY_URL'] = privacy_policy['link']
        elif privacy_policy['text']:
            legal_context['PRIVACY_POLICY_URL'] = reverse('misago:privacy-policy')

    if legal_context:
        request.frontend_context.update(legal_context)

    return legal_context
