from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import six
from django.views import View

from misago.core.utils import format_plaintext_for_html
from misago.users.models import Rank
from misago.users.pages import users_list
from misago.users.permissions import allow_browse_users_list
from misago.users.viewmodels import ActivePosters, RankUsers


class ListView(View):
    def get(self, request, *args, **kwargs):
        allow_browse_users_list(request.user)

        context_data = self.get_context_data(request, *args, **kwargs)

        context_data['pages'] = users_list.get_sections(request)

        request.frontend_context['USERS_LISTS'] = []
        for page in context_data['pages']:
            page['reversed_link'] = reverse(page['link'])
            request.frontend_context['USERS_LISTS'].append({
                'name': six.text_type(page['name']),
                'component': page['component'],
            })

        active_rank = context_data.get('rank')
        for rank in Rank.objects.filter(is_tab=True).order_by('order'):
            context_data['pages'].append({
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

        for page in context_data['pages']:
            if page['is_active']:
                context_data['active_page'] = page
                break

        return render(request, self.template_name, context_data)

    def get_context_data(self, request, *args, **kwargs):
        return {}


def landing(request):
    allow_browse_users_list(request.user)
    return redirect(users_list.get_default_link())


class ActivePostersView(ListView):
    template_name = 'misago/userslists/active_posters.html'

    def get_context_data(self, request, *args, **kwargs):
        model = ActivePosters(request)

        request.frontend_context['USERS'] = model.get_frontend_context()

        return model.get_template_context()


class RankUsersView(ListView):
    template_name = 'misago/userslists/rank.html'

    def get_context_data(self, request, slug, page=0):
        rank = get_object_or_404(Rank.objects.filter(is_tab=True), slug=slug)
        users = RankUsers(request, rank, page)

        request.frontend_context['USERS'] = users.get_frontend_context()

        context = {
            'rank': rank,
        }
        context.update(users.get_template_context())

        return context
