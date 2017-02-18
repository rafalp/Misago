from django.contrib.auth import get_user_model
from django.shortcuts import render as django_render
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import six

from misago.conf import settings
from misago.core.shortcuts import paginate, pagination_dict
from misago.core.utils import format_plaintext_for_html
from misago.users.models import Rank
from misago.users.pages import users_list
from misago.users.permissions import allow_browse_users_list
from misago.users.serializers import UserCardSerializer
from misago.users.viewmodels import ActivePosters, RankUsers


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
    model = ActivePosters(request)

    request.frontend_context['USERS'] = model.get_frontend_context()

    template = "misago/userslists/active_posters.html"
    return render(request, template, model.get_template_context())


@allow_see_list
def rank_users(request, slug, page=0):
    rank = get_object_or_404(Rank.objects.filter(is_tab=True), slug=slug)
    users = RankUsers(request, rank, page)

    request.frontend_context['USERS'] = users.get_frontend_context()

    context = {
        'rank': rank,
    }
    context.update(users.get_template_context())

    return render(request, "misago/userslists/rank.html", context)


ScoredUserSerializer = UserCardSerializer.extend_fields('meta')
