from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render

from misago.legal.models import LegalAgreement
from misago.markup import common_flavour

def legals_active(request):
    legal_active = LegalAgreement.objects.filter(is_active=True).all()
    response = HttpResponse(" \n".join(str(v) for v in list(legal_active)))
    response['Content-Type'] = 'text/plain'

    return response

def legal_title(request, title):
    """
    This function returns the active specified legal type
    :param title: Legal Type name.
    :return: legal.text
    """
    try:
        legal = LegalAgreement.objects.filter(is_active=True).get(title=title)
    except LegalAgreement.DoesNotExist:
        raise Http404

    parsed = common_flavour(request, None, legal.text)

    return render(
        request, 'misago/legal.html', {
            'id': legal.title,
            'title': dict(legal.LEGAL_CHOICES)[legal.title],
            'body': parsed,
        }
