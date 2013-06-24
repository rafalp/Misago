from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet, RelatedSearchQuerySet
from misago.acl.exceptions import ACLError403, ACLError404
from misago.decorators import block_crawlers
from misago.forms import FormFields
from misago.models import Forum, Thread, Post, User
from misago.search import SearchException
from misago.utils.pagination import make_pagination
from misago.apps.errors import error403, error404
from misago.apps.profiles.views import list as users_list
from misago.apps.search.forms import QuickSearchForm

class ViewBase(object):
    search_route = 'search'

    def check_acl(self):
        pass

    def make_query(self, search_query):
        sqs = SearchQuerySet()
        if self.request.POST.get('search_thread_titles'):
            sqs = sqs.filter(thread_name=AutoQuery(search_query))
        else:
            sqs = sqs.auto_query(search_query)

        if self.request.POST.get('search_in') == 'private':
            if not (self.request.acl.private_threads.can_participate()
                    and self.request.settings['enable_private_threads']):
                raise ACLError404()
            sqs = sqs.filter(thread__in=[t.pk for t in self.request.user.private_thread_set.all()])
        elif self.request.POST.get('search_in') == 'reports':
            if not self.request.acl.reports.can_handle():
                raise ACLError404()
            sqs = sqs.filter(forum=Forum.objects.special_pk('reports'))
        elif self.request.POST.get('search_in') == 'thread':
            try:
                thread_id = int(self.request.POST.get('search_thread'))
                thread_clean = Thread.objects.get(id=thread_id)
                if not thread_clean.forum_id in Forum.objects.readable_forums(self.request.acl, True):
                    raise ACLError404()
                self.thread_clean = thread_clean
                sqs = sqs.filter(thread=thread_clean.pk)
            except (TypeError, Thread.DoesNotExist):
                raise ACLError404()
        else:
            sqs = sqs.filter(forum__in=Forum.objects.readable_forums(self.request.acl))

        if self.request.POST.get('search_author'):
            sqs = sqs.filter(author__exact=self.request.POST.get('search_author'))

        return sqs

    def render_to_response(self, template, form, context):
        for i in ('search_query', 'search_in', 'search_author', 'search_thread_titles'):
            if self.request.POST.get(i):
                context[i] = self.request.POST.get(i)
        try:
            context['search_thread'] = self.thread_clean
        except AttributeError:
            pass
        return self.request.theme.render_to_response('search/%s.html' % template,
                                                     context,
                                                     context_instance=RequestContext(self.request))

    def __new__(cls, request, **kwargs):
        obj = super(ViewBase, cls).__new__(cls)
        return obj(request, **kwargs)

    def __call__(self, request, **kwargs):
        try:
            if request.user.is_crawler():
                raise ACLError404()
            self.check_acl()
            if not request.acl.search.can_search():
                raise ACLError403(_("You don't have permission to search community."))
            self.request = request
            return self.call(**kwargs)
        except ACLError403 as e:
            return error403(request, unicode(e))
        except ACLError404 as e:
            return error404(request, unicode(e))


class QuickSearchView(ViewBase):
    def call(self, **kwargs):
        form_type = QuickSearchForm
        if self.request.method != "POST":
            form = QuickSearchForm(request=self.request)
            return self.render_to_response('home', form,
                                           {'search_result': self.request.session.get('search_results')})
        
        try:
            form = QuickSearchForm(self.request.POST, request=self.request)
            if form.is_valid():
                if form.mode == 'forum':
                    jump_to = Forum.objects.forum_by_name(form.target, self.request.acl)
                    if jump_to:
                        if jump_to.level == 1:
                            return redirect(reverse('index') + ('#%s' % jump_to.slug))
                        return redirect(jump_to.url)
                    else:
                        raise SearchException(_('Forum "%(forum)s" could not be found.') % {'forum': form.target})
                if form.mode == 'user':
                    self.request.POST = self.request.POST.copy()
                    self.request.POST['username'] = form.target
                    return users_list(self.request)

                sqs = self.make_query(form.cleaned_data['search_query']).load_all()[:60]

                if self.request.user.is_authenticated():
                    self.request.user.last_search = timezone.now()
                    self.request.user.save(force_update=True)
                if self.request.user.is_anonymous():
                    self.request.session['last_search'] = timezone.now()

                if not sqs:
                    raise SearchException(_("Search returned no results. Change search query and try again."))

                self.request.session['search_results'] = {
                                                          'search_query': form.cleaned_data['search_query'],
                                                          'search_in': self.request.POST.get('search_in'),
                                                          'search_author': self.request.POST.get('search_author'),
                                                          'search_thread_titles': self.request.POST.get('search_thread_titles'),
                                                          'search_results': [p.object for p in sqs],
                                                          }
                try:
                    self.request.session['search_results']['search_thread'] = self.thread_clean
                except AttributeError:
                    pass
                return redirect(reverse('search_results'))
            else:
                if 'search_query' in form.errors:
                    raise SearchException(form.errors['search_query'][0])
                raise SearchException(form.errors['__all__'][0])
        except SearchException as e:
            return self.render_to_response('error', form,
                                           {'message': unicode(e)})


class SearchResultsView(ViewBase):
    def call(self, **kwargs):
        result = self.request.session.get('search_results')
        if not result:
            form = QuickSearchForm(request=self.request)
            return self.render_to_response('error', form,  
                                           {'message': _("No search results were found.")})

        items = result['search_results']
        items_total = len(items);
        try:
            pagination = make_pagination(kwargs.get('page', 0), items_total, 12)
        except Http404:
            return redirect(reverse('search_results'))

        form = QuickSearchForm(request=self.request, initial={'search_query': result['search_query']})
        return self.render_to_response('results', form,  
                                       {
                                        'search_query': result['search_query'],
                                        'search_in': result.get('search_in'),
                                        'search_author': result.get('search_author'),
                                        'search_thread_titles': result.get('search_thread_titles'),
                                        'search_thread': result.get('search_thread'),
                                        'results': items[pagination['start']:pagination['stop']],
                                        'items_total': items_total,
                                        'pagination': pagination,
                                       })