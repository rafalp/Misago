from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from misago.legal.models import Agreement
from misago.legal.utils import get_parsed_content


def legal_view(request, agreement_type):
    agreement = get_object_or_404(
        Agreement, type=agreement_type, is_active=True
    )

    if agreement.link:
        return redirect(agreement.link)

    template_name = 'misago/{}.html'.format(agreement_type)
    parsed_content = get_parsed_content(request, agreement)

    return render(
        request,
        template_name,
        {
            'id': slugify(agreement_type),
            'title': agreement.get_final_title(),
            'link': agreement.link,
            'body': parsed_content,
            'hide_misago_agreement': True,
        }
    )


def privacy_policy(request):
    return legal_view(request, Agreement.TYPE_PRIVACY)


def terms_of_service(request):
    return legal_view(request, Agreement.TYPE_TOS)
