from .models import Agreement


def set_agreement_as_active(agreement, commit=False):
    agreement.is_active = True
    queryset = Agreement.objects.filter(type=agreement.type).exclude(pk=agreement.pk)
    queryset.update(is_active=False)
    agreement.save(update_fields=['is_active'])
    Agreement.objects.invalidate_cache()