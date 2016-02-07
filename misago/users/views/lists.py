from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.shortcuts import redirect, render as django_render
from django.utils import timezone

from misago.forums.models import Forum
from misago.core.cache import cache
from misago.core.shortcuts import get_object_or_404, paginate, pagination_dict
from misago.core.utils import format_plaintext_for_html

from misago.users.models import Rank
from misago.users.pages import users_list
from misago.users.permissions.profiles import allow_browse_users_list
from misago.users.serializers import UserSerializer, ScoredUserSerializer


def render(request, template, context):
    request.frontend_context['USERS_LISTS'] = []

    context['pages'] = users_list.get_sections(request)

    for page in context['pages']:
        page['reversed_link'] = reverse(page['link'])
        request.frontend_context['USERS_LISTS'].append({
            'name': unicode(page['name']),
            'component': page['component'],
        })

    active_rank = context.get('rank')
    for rank in Rank.objects.filter(is_tab=True).order_by('order'):
        context['pages'].append({
            'name': rank.name,
            'reversed_link': reverse('misago:users_rank',
                                     kwargs={'rank_slug': rank.slug}),
            'is_active': active_rank.pk == rank.pk if active_rank else None
        })

        if rank.description:
            description = {
                'plain': rank.description,
                'html': format_plaintext_for_html(rank.description)
            }
        else:
            description = None

        request.frontend_context['USERS_LISTS'].append({
            'name': rank.name,
            'slug': rank.slug,
            'css_class': rank.css_class,
            'description': description,
            'component': 'rank',
        })

    for page in context['pages']:
        if page['is_active']:
            context['active_page'] = page
            break

    return django_render(request, template, context)


def allow_see_list(f):
    def decorator(request, *args, **kwargs):
        allow_browse_users_list(request.user)
        return f(request, *args, **kwargs)
    return decorator


@allow_see_list
def lander(request):
    default = users_list.get_default_link()
    return redirect(default)


@allow_see_list
def active_posters(request):
    ranking = get_active_posters_rankig()

    request.frontend_context['USERS'] = {
        'tracked_period': settings.MISAGO_RANKING_LENGTH,
        'results': ScoredUserSerializer(ranking['users'], many=True).data,
        'count': ranking['users_count']
    }

    template = "misago/userslists/active_posters.html"
    return render(request, template, {
        'tracked_period': settings.MISAGO_RANKING_LENGTH,
        'users': ranking['users'],
        'users_count': ranking['users_count']
    })


def get_active_posters_rankig():
    cache_key = 'misago_active_posters_ranking'
    ranking = cache.get(cache_key, 'nada')
    if ranking == 'nada':
        ranking = get_real_active_posts_ranking()
        cache.set(cache_key, ranking, 18*3600)
    return ranking


def get_real_active_posts_ranking():
    tracked_period = settings.MISAGO_RANKING_LENGTH
    tracked_since = timezone.now() - timedelta(days=tracked_period)

    ranked_forums = [forum.pk for forum in Forum.objects.all_forums()]

    User = get_user_model()
    queryset = User.objects.filter(posts__gt=0)
    queryset = queryset.filter(post__posted_on__gte=tracked_since,
                               post__forum__in=ranked_forums)
    queryset = queryset.annotate(score=Count('post'))
    queryset = queryset.select_related('user__rank')
    queryset = queryset.order_by('-score')

    queryset = queryset[:settings.MISAGO_RANKING_SIZE]

    return {
        'users': [user for user in queryset],
        'users_count': queryset.count()
    }


@allow_see_list
def rank(request, rank_slug, page=0):
    rank = get_object_or_404(Rank.objects.filter(is_tab=True), slug=rank_slug)
    queryset = rank.user_set.select_related('rank').order_by('slug')

    page = paginate(queryset, page, settings.MISAGO_USERS_PER_PAGE, 4)
    paginator = pagination_dict(page)

    request.frontend_context['USERS'] = dict(
        results=UserSerializer(page.object_list, many=True).data,
        **paginator
    )

    if rank.description:
        description = {
            'plain': rank.description,
            'html': format_plaintext_for_html(rank.description)
        }
    else:
        description = None

    template = "misago/userslists/rank.html"
    return render(request, template, {
        'rank': rank,
        'users': page.object_list,

        'paginator': paginator
    })
