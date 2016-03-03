from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone

from misago.categories.models import Category
from misago.core.cache import cache


ACTIVE_POSTERS_CACHE = 'misago_active_posters_ranking'


def get_active_posters_ranking():
    ranking = cache.get(ACTIVE_POSTERS_CACHE, 'nada')
    if ranking == 'nada':
        ranking = get_real_active_posts_ranking()
        cache.set(ACTIVE_POSTERS_CACHE, ranking, 18*3600)
    return ranking


def get_real_active_posts_ranking():
    tracked_period = settings.MISAGO_RANKING_LENGTH
    tracked_since = timezone.now() - timedelta(days=tracked_period)

    ranked_categories = []
    for category in Category.objects.all_categories():
        ranked_categories.append(category.pk)

    User = get_user_model()
    queryset = User.objects.filter(posts__gt=0)
    queryset = queryset.filter(post__posted_on__gte=tracked_since,
                               post__category__in=ranked_categories)
    queryset = queryset.annotate(score=Count('post'))
    queryset = queryset.select_related('rank')
    queryset = queryset.order_by('-score')

    users = list(queryset[:settings.MISAGO_RANKING_SIZE])

    return {
        'users': users,
        'users_count': len(users),
    }


def clear_active_posters_ranking():
    cache.delete(ACTIVE_POSTERS_CACHE)