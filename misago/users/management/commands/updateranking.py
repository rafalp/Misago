from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from optparse import make_option
from misago.users.models import User, Rank

class Command(BaseCommand):
    """
    This command is intended to work as CRON job fired of once per day or less if you have more users to update user ranking.
    """
    help = 'Updates users ranking'
    def handle(self, *args, **options):
        # Find special ranks
        special_ranks = []
        for rank in Rank.objects.filter(special=1):
            special_ranks.append(str(rank.pk))
        
        # Count users that are in ranking
        users_total = User.objects.exclude(rank__in=special_ranks).count()
        
        # Update Ranking
        defaulted_ranks = False
        for rank in Rank.objects.filter(special=0).order_by('order'):
            if defaulted_ranks:
                # Set ranks according to ranking
                rank.assign_rank(users_total, special_ranks)
            else:
                # Set default rank first
                Users.objects.exclude(rank__in=special_ranks).update(rank=rank)
                defaulted_ranks = True
        
        self.stdout.write('Users ranking for has been updated.\n')