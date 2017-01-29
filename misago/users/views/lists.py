import six

from django.contrib.auth import get_user_model
from django.shortcuts import render as django_render
from django.shortcuts import redirect
from django.urls import reverse

from misago.conf import settings
from misago.core.shortcuts import get_object_or_404, paginate, pagination_dict
from misago.core.utils import format_plaintext_for_html

from ..activepostersranking import get_active_posters_ranking
from ..models import Rank
from ..pages import users_list
from ..permissions.profiles import allow_browse_users_list
from ..serializers import ScoredUserSerializer, UserSerializer


def render(request, template, context):
    request.frontend_context['USERS_LISTS'] = []

    context['pages'] = users_list.get_sections(request)

    for page in context['pages']:
        page['reversed_link'] = reverse(page['link'])
        request.frontend_context['USERS_LISTS'].append({
            'name': six.text_type(page['name']),
            'component': page['component'],
        })

    active_rank = context.get('rank')
    for rank in Rank.objects.filter(is_tab=True).order_by('order'):
        context['pages'].append({
            'name': rank.name,
            'reversed_link': reverse('misago:users-rank', kwargs={
                'slug': rank.slug
            }),
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
            'id': rank.pk,
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
def landing(request):
    default = users_list.get_default_link()
    return redirect(default)


@allow_see_list
def active_posters(request):
    ranking = get_active_posters_ranking()

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


@allow_see_list
def rank(request, slug, page=0):
    rank = get_object_or_404(Rank.objects.filter(is_tab=True), slug=slug)
    queryset = rank.user_set.select_related('rank').order_by('slug')

    if not request.user.is_staff:
        queryset = queryset.filter(is_active=True)

    page = paginate(queryset, page, settings.MISAGO_USERS_PER_PAGE, 4)

    data = pagination_dict(page)
    data.update({
        'results': UserSerializer(page.object_list, many=True).data
    })

    request.frontend_context['USERS'] = data

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

        'paginator': data
    })
