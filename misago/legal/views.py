from django.shortcuts import get_object_or_404, redirect, render

from .models import Agreement
from .utils import get_parsed_agreement_text


def legal_view(request, agreement_type):
    agreement = get_object_or_404(Agreement, type=agreement_type, is_active=True)

    if agreement.link:
        return redirect(agreement.link)

    template_name = "misago/%s.html" % agreement_type
    agreement_text = get_parsed_agreement_text(request, agreement)

    return render(
        request,
        template_name,
        {
            "title": agreement.get_final_title(),
            "link": agreement.link,
            "text": agreement_text,
        },
    )


def privacy_policy(request):
    return legal_view(request, Agreement.TYPE_PRIVACY)


def terms_of_service(request):
    return legal_view(request, Agreement.TYPE_TOS)
