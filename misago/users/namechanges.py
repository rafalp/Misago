"""
Service for tracking namechanges
"""
from datetime import timedelta

from django.utils import timezone

from .models import UsernameChange


class UsernameChanges(object):
    def __init__(self, user):
        self.left = 0
        self.next_on = None

        if user.acl_cache['name_changes_allowed']:
            self.count_namechanges(user)

    def count_namechanges(self, user):
        name_changes_allowed = user.acl_cache['name_changes_allowed']
        name_changes_expire = user.acl_cache['name_changes_expire']

        valid_changes_qs = user.namechanges.filter(changed_by=user)
        if name_changes_expire:
            cutoff = timezone.now() - timedelta(days=name_changes_expire)
            valid_changes_qs = valid_changes_qs.filter(changed_on__gte=cutoff)

        used_changes = valid_changes_qs.count()
        if name_changes_allowed <= used_changes:
            self.left = 0
        else:
            self.left = name_changes_allowed - used_changes

        if not self.left and name_changes_expire:
            try:
                self.next_on = valid_changes_qs.latest().changed_on
                self.next_on += timedelta(days=name_changes_expire)
            except UsernameChange.DoesNotExist:
                pass
