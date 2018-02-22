from datetime import timedelta

from django.utils import timezone

from .models import UsernameChange


def get_available_namechanges_data(user):
    namechanges_data = {
        'changes_left': 0,
        'next_change_on': None,
    }

    if not user.acl_cache['name_changes_allowed']:
        return namechanges_data

    name_changes_allowed = user.acl_cache['name_changes_allowed']
    name_changes_expire = user.acl_cache['name_changes_expire']

    valid_changes_qs = user.namechanges.filter(changed_by=user)
    if name_changes_expire:
        cutoff = timezone.now() - timedelta(days=name_changes_expire)
        valid_changes_qs = valid_changes_qs.filter(changed_on__gte=cutoff)

    used_changes = valid_changes_qs.count()
    if name_changes_allowed > used_changes:
        namechanges_data['changes_left'] = name_changes_allowed - used_changes

    if not namechanges_data['changes_left'] and name_changes_expire:
        try:
            namechanges_data['next_change_on'] = valid_changes_qs.latest().changed_on
            namechanges_data['next_change_on'] += timedelta(days=name_changes_expire)
        except UsernameChange.DoesNotExist:
            pass
    
    return namechanges_data
