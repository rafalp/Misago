from hashlib import md5

from django.conf import settings
from django.core.cache import cache
from django.utils.encoding import force_bytes

from ..markup import common_flavour
from .models import Agreement, UserAgreement


def get_required_user_agreement(user, agreements):
    if user.is_anonymous:
        return None

    for agreement_type, _ in Agreement.TYPE_CHOICES:
        agreement = agreements.get(agreement_type)
        if agreement and agreement["id"] not in user.agreements:
            try:
                return Agreement.objects.get(id=agreement["id"])
            except Agreement.DoesNotExist:
                # possible stale cache
                Agreement.invalidate_cache()


def get_parsed_agreement_text(request, agreement):
    if not agreement.text:
        return None

    cache_name = "misago_legal_%s_%s" % (agreement.pk, agreement.last_modified_on or "")
    cached_content = cache.get(cache_name)

    unparsed_content = agreement.text

    checksum_source = force_bytes("%s:%s" % (unparsed_content, settings.SECRET_KEY))
    unparsed_checksum = md5(checksum_source).hexdigest()

    if cached_content and cached_content.get("checksum") == unparsed_checksum:
        return cached_content["parsed"]

    parsed = common_flavour(request, None, unparsed_content)["parsed_text"]
    cached_content = {"checksum": unparsed_checksum, "parsed": parsed}
    cache.set(cache_name, cached_content)
    return cached_content["parsed"]


def save_user_agreement_acceptance(user, agreement, commit=False):
    user.agreements.append(agreement.id)
    UserAgreement.objects.create(agreement=agreement, user=user)

    if commit:
        user.save(update_fields=["agreements"])
