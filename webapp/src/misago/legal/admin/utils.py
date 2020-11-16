from ..models import Agreement


def set_agreement_as_active(agreement, commit=False):
    agreement.is_active = True
    Agreement.objects.filter(type=agreement.type).exclude(pk=agreement.pk).update(
        is_active=False
    )

    if commit:
        agreement.save(update_fields=["is_active"])
        Agreement.objects.invalidate_cache()


def disable_agreement(agreement, commit=False):
    agreement.is_active = False
    if commit:
        agreement.save(update_fields=["is_active"])
        Agreement.objects.invalidate_cache()
