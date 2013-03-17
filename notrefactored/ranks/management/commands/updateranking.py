from django.core.management.base import BaseCommand, CommandError
from django.db.models import F
from misago.settings.settings import Settings
from misago.ranks.models import Rank
from misago.users.models import User

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
                User.objects.exclude(rank__in=special_ranks).update(rank=rank)
                defaulted_ranks = True

        # Inflate scores
        settings = Settings()
        inflation = float(100 - settings['ranking_inflation']) / 100
        User.objects.all().update(score=F('score') * inflation, ranking=0)

        self.stdout.write('Users ranking for has been updated.\n')
