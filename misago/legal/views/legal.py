from hashlib import md5

from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import force_bytes
from django.utils.text import slugify

from misago.core.cache import cache
from misago.legal.models import Agreement
from misago.markup import common_flavour


def get_parsed_content(request, agreement):
    cache_name = 'misago_legal_%s_%s' % (agreement.pk, agreement.last_modified_on or '')
    cached_content = cache.get(cache_name)

    unparsed_content = agreement.text

    checksum_source = force_bytes('%s:%s' % (unparsed_content, settings.SECRET_KEY))
    unparsed_checksum = md5(checksum_source).hexdigest()

    if cached_content and cached_content.get('checksum') == unparsed_checksum:
        return cached_content['parsed']
    else:
        parsed = common_flavour(request, None, unparsed_content)['parsed_text']
        cached_content = {
            'checksum': unparsed_checksum,
            'parsed': parsed,
        }
        cache.set(cache_name, cached_content)
        return cached_content['parsed']


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
        }
    )


def privacy_policy(request):
    return legal_view(request, Agreement.TYPE_PRIVACY)


def terms_of_service(request):
    return legal_view(request, Agreement.TYPE_TOS)
