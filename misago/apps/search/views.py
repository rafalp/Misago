from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from haystack.query import RelatedSearchQuerySet
from misago.decorators import block_crawlers
from misago.forms import FormFields
from misago.models import Forum, Thread, Post, User
from misago.search import SearchException
from misago.apps.errors import error403, error404
from misago.apps.profiles.views import list as users_list
from misago.apps.search.forms import QuickSearchForm

@block_crawlers
def search(request):
    queryset = Post.objects.filter(forum__in=Forum.objects.readable_forums(request.acl))
    return do_search(request, queryset)


def do_search(request, queryset, search_route=None):
    if not request.acl.search.can_search():
        return error403(request, _("You don't have permission to search community."))

    search_route = search_route or 'search'

    if request.method != "POST":
        form = QuickSearchForm(request=request)
        return request.theme.render_to_response('search/home.html',
                                                {
                                                 'form': FormFields(form),
                                                 'search_route': search_route,
                                                 'search_result': request.session.get('%s_result' % search_route),
                                                 'disable_search': True,
                                                },
                                                context_instance=RequestContext(request))
        
    try:
        form = QuickSearchForm(request.POST, request=request)
        if form.is_valid():
            if form.mode == 'forum':
                jump_to = Forum.objects.forum_by_name(form.target, request.acl)
                if jump_to:
                    if jump_to.level == 1:
                        return redirect(reverse('index') + ('#%s' % jump_to.slug))
                    return redirect(jump_to.url)
                else:
                    raise SearchException(_('Forum "%(forum)s" could not be found.') % {'forum': form.target})
            if form.mode == 'user':
                request.POST = request.POST.copy()
                request.POST['username'] = form.target
                return users_list(request)
            sqs = RelatedSearchQuerySet().auto_query(form.cleaned_data['search_query']).order_by('-id').load_all()
            sqs = sqs.load_all_queryset(Post, queryset.select_related('thread', 'forum'))[:24]
            request.user.last_search = timezone.now()
            request.user.save(force_update=True)
            if not sqs:
                raise SearchException(_("Search returned no results. Change search query and try again."))
            request.session['%s_result' % search_route] = {
                                                           'search_query': form.cleaned_data['search_query'],
                                                           'search_results': [p.object.pk for p in sqs],
                                                           }
            return redirect(reverse('%s_results' % search_route))
        else:
            raise SearchException(form.errors['search_query'][0])
    except SearchException as e:
        return request.theme.render_to_response('search/error.html',
                                                {
                                                 'form': FormFields(form),
                                                 'search_route': search_route,
                                                 'message': unicode(e),
                                                 'disable_search': True,
                                                },
                                                context_instance=RequestContext(request))


@block_crawlers
def show_results(request):
    return results(request)


def results(request, search_route=None):
    if not request.acl.search.can_search():
        return error403(request, _("You don't have permission to search community."))

    search_route = search_route or 'search'
    result = request.session.get('%s_result' % search_route)
    if not result:
        form = QuickSearchForm(request=request)
        return request.theme.render_to_response('search/error.html',
                                                {
                                                 'form': FormFields(form),
                                                 'search_route': search_route,
                                                 'message': _("No search results were found."),
                                                 'disable_search': True,
                                                },
                                                context_instance=RequestContext(request))

    form = QuickSearchForm(request=request, initial={'search_query': result['search_query']})
    return request.theme.render_to_response('search/results.html',
                                            {
                                             'form': FormFields(form),
                                             'search_route': search_route,
                                             'search_query': result['search_query'],
                                             'results': Post.objects.filter(id__in=result['search_results']).select_related('thread', 'forum', 'user'),
                                             'disable_search': True,
                                            },
                                            context_instance=RequestContext(request))

