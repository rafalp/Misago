from hashlib import md5

from django.conf import settings
from django.utils.encoding import force_bytes

from misago.core.cache import cache
from misago.markup import common_flavour

from .models import Agreement


def set_agreement_as_active(agreement, commit=False):
    agreement.is_active = True
    queryset = Agreement.objects.filter(type=agreement.type).exclude(pk=agreement.pk)
    queryset.update(is_active=False)
    agreement.save(update_fields=['is_active'])
    Agreement.objects.invalidate_cache()


def get_required_user_agreement(user, agreements):
    if user.is_anonymous:
        return None

    for agreement in agreements.values():
        if agreement['id'] not in user.agreements:
            try:
                return Agreement.objects.get(id=agreement['id'])
            except Agreement.DoesNotExist:
                # possible stale cache
                Agreement.invalidate_cache()
    
    return None


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
