from django.urls import reverse

from .models import Agreement
from .utils import get_parsed_agreement_text, get_required_user_agreement

# fixme: rename this context processor to more suitable name
def legal_links(request):
    agreements = Agreement.objects.get_agreements()

    legal_context = {
        "TERMS_OF_SERVICE_ID": None,
        "TERMS_OF_SERVICE_URL": None,
        "PRIVACY_POLICY_ID": None,
        "PRIVACY_POLICY_URL": None,
        "misago_agreement": None,
    }

    terms_of_service = agreements.get(Agreement.TYPE_TOS)
    if terms_of_service:
        legal_context["TERMS_OF_SERVICE_ID"] = terms_of_service["id"]
        if terms_of_service["link"]:
            legal_context["TERMS_OF_SERVICE_URL"] = terms_of_service["link"]
        elif terms_of_service["text"]:
            legal_context["TERMS_OF_SERVICE_URL"] = reverse("misago:terms-of-service")

    privacy_policy = agreements.get(Agreement.TYPE_PRIVACY)
    if privacy_policy:
        legal_context["PRIVACY_POLICY_ID"] = privacy_policy["id"]
        if privacy_policy["link"]:
            legal_context["PRIVACY_POLICY_URL"] = privacy_policy["link"]
        elif privacy_policy["text"]:
            legal_context["PRIVACY_POLICY_URL"] = reverse("misago:privacy-policy")

    if legal_context:
        request.frontend_context.update(legal_context)

    required_agreement = get_required_user_agreement(request.user, agreements)
    if required_agreement:
        request.frontend_context["REQUIRED_AGREEMENT_API"] = reverse(
            "misago:api:submit-agreement", kwargs={"pk": required_agreement.pk}
        )

        legal_context["misago_agreement"] = {
            "type": required_agreement.get_type_display(),
            "title": required_agreement.get_final_title(),
            "link": required_agreement.link,
            "text": get_parsed_agreement_text(request, required_agreement),
        }

    return legal_context
