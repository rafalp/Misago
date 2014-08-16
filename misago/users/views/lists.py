import warnings

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render as django_render
from django.utils import timezone
from django.views.decorators.cache import cache_page

from misago.core.shortcuts import get_object_or_404, paginate

from misago.users.models import Rank
from misago.users.online.utils import get_online_queryset
from misago.users.permissions.profiles import (allow_browse_users_list,
                                               allow_see_users_online_list)
from misago.users.sites import users_list


def render(request, template, context):
    context['pages'] = users_list.get_pages(request)

    for page in context['pages']:
        page['reversed_link'] = reverse(page['link'])

    active_rank = context.get('rank')
    for rank in Rank.objects.filter(is_tab=True).order_by('order'):
        context['pages'].append({
            'name': rank.name,
            'reversed_link': reverse('misago:users_rank',
                                     kwargs={'rank_slug': rank.slug}),
            'is_active': active_rank.pk == rank.pk if active_rank else None
        })

    for page in context['pages']:
        if page['is_active']:
            context['active_page'] = page
            break

    return django_render(request, template, context)


def allow_see_list(permission=None):
    def permission_decorator(f):
        def decorator(request, *args, **kwargs):
            allow_browse_users_list(request.user)
            if permission:
                permission(request.user)
            return f(request, *args, **kwargs)
        return decorator
    return permission_decorator


@allow_see_list()
def lander(request):
    default = users_list.get_default_link()
    return redirect(default)


def list_view(request, template, queryset, page, context=None):
    context = context or {}
    context['users'] = paginate(queryset, page, 6 * 3, 5)
    return render(request, template, context)


@allow_see_list()
@cache_page(24 * 3600)
def active_posters(request, page=0):
    warnings.warn("Not implemented yet! See #404 for details.",
                  FutureWarning)

    tracked_period = settings.MISAGO_RANKING_LENGTH
    User = get_user_model()
    queryset = User.objects.all().select_related('user__rank')

    template = "misago/userslists/active_posters.html"
    return list_view(request, template, queryset, page, {
        'tracked_period': tracked_period
    })


@allow_see_list(allow_see_users_online_list)
def online(request, page=0):
    queryset = get_online_queryset(request.user).order_by('user__slug')
    queryset = queryset.select_related('user__rank')

    template = "misago/userslists/online.html"
    return list_view(request, template, queryset, page, {
        'data_from': timezone.now()
    })


@allow_see_list()
def rank(request, rank_slug, page=0):
    rank = get_object_or_404(Rank.objects.filter(is_tab=True), slug=rank_slug)
    queryset = rank.user_set.order_by('slug')

    template = "misago/userslists/rank.html"
    return list_view(request, template, queryset, page, {'rank': rank})
