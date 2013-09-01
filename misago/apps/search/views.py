from urlparse import urlparse
from django.core.urlresolvers import reverse, resolve
from django.http import Http404
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet, RelatedSearchQuerySet
from misago.acl.exceptions import ACLError403, ACLError404
from misago.conf import settings
from misago.decorators import block_crawlers
from misago.messages import Message
from misago.models import Forum, Thread, Post, User
from misago.search import SearchException, MisagoSearchQuerySet
from misago.shortcuts import render_to_response
from misago.utils.pagination import make_pagination
from misago.apps.errors import error403, error404
from misago.apps.profiles.views import list as users_list
from misago.apps.search.forms import (QuickSearchForm, ForumsSearchForm,
                                      PrivateThreadsSearchForm, ReportsSearchForm)

class ViewBase(object):
    def check_acl(self):
        pass

    def make_query(self, search_data):
        try:
            sqs = MisagoSearchQuerySet(self.request.user, self.request.acl)
            if self.search_route == 'search_private_threads':
                sqs.allow_forum_search(Forum.objects.special_model('private_threads'))
            elif self.search_route == 'search_reports':
                sqs.allow_forum_search(Forum.objects.special_model('reports'))
            else:
                if search_data.get('search_forums'):
                    if search_data.get('search_forums_childs'):
                        forums_tree = Forum.objects.forums_tree
                        readable_forums = Forum.objects.readable_forums(self.request.acl)

                        ranges = []
                        for forum in search_data.get('search_forums'):
                            if not ranges or ranges[-1][1] < forum.rght:
                                ranges.append((forum.lft, forum.rght))

                        forums = []
                        for rang in ranges:
                            for pk, forum in forums_tree.items():
                                if pk in readable_forums:
                                    if forum.lft >= rang[0] and forum.rght <= rang[1]:
                                        forums.append(pk)
                                    if forum.lft > rang[1]:
                                        break

                        sqs.in_forums(forums)
                    else:
                        sqs.in_forums([f.pk for f in search_data.get('search_forums')])
                else:
                    sqs.in_forums(Forum.objects.readable_forums(self.request.acl))

            if search_data.get('search_thread_titles'):
                sqs.search_thread_name(search_data.get('search_query'))
                sqs.search_thread_titles()
            else:
                sqs.search_content(search_data.get('search_query'))

            if search_data.get('search_thread'):
                sqs.search_thread_name_link(search_data.get('search_thread'))

            if search_data.get('search_author'):
                sqs.search_user_name(search_data.get('search_author'))

            if search_data.get('search_before'):
                sqs.search_before(search_data.get('search_before'))

            if search_data.get('search_after'):
                sqs.search_after(search_data.get('search_after'))

            return sqs
        except Thread.DoesNotExist:
            raise ACLError404()

    def render_to_response(self, template, form, context):
        context['search_route'] = self.search_route
        context['form'] = form
        for i in ('search_query', 'search_in', 'search_author', 'search_thread_titles'):
            if self.request.POST.get(i):
                context[i] = self.request.POST.get(i)
        try:
            context['search_thread'] = self.thread_clean
        except AttributeError:
            pass
        return render_to_response('search/%s.html' % template,
                                  context,
                                  context_instance=RequestContext(self.request))

    def draw_form(self, request):
        search_form_data = self.request.session.get('search_form_data')
        if search_form_data and search_form_data['form'] == self.search_route:
            form = self.search_form(request=self.request, initial=search_form_data['data'])
        else:
            form = self.search_form(request=self.request)
        return self.render_to_response(self.search_route, form,
                                       {'search_result': self.request.session.get('search_results')})

    def search(self, request):
        self.request.session['search_form_data'] = None
        message = None

        # Hackish interception of quick search form
        if self.search_route == 'search_quick':
            if self.request.POST.get('search_in') == 'thread':
                try:
                    link = resolve(urlparse(self.request.POST.get('search_thread')).path)
                    search_thread = Thread.objects.get(pk=link.kwargs['thread'])
                    self.request.acl.threads.allow_thread_view(self.request.user, search_thread)
                    if search_thread.forum_id == Forum.objects.special_pk('private_threads'):
                        self.search_route = 'search_private_threads'
                        self.search_form = PrivateThreadsSearchForm
                    elif search_thread.forum_id == Forum.objects.special_pk('reports'):
                        self.search_route = 'search_reports'
                        self.search_form = ReportsSearchForm
                    else:
                        self.search_route = 'search_forums'
                        self.search_form = ForumsSearchForm
                except (Http404, KeyError, Thread.DoesNotExist):
                    raise ACLError404()
            elif self.request.POST.get('search_in') in ('forums', 'private_threads', 'reports'):
                if self.request.POST.get('search_in') == 'forums':
                    self.search_route = 'search_forums'
                    self.search_form = ForumsSearchForm
                elif self.request.POST.get('search_in') == 'private_threads':
                    self.search_route = 'search_private_threads'
                    self.search_form = PrivateThreadsSearchForm
                elif self.request.POST.get('search_in') == 'reports':
                    self.search_route = 'search_reports'
                    self.search_form = ReportsSearchForm

        form = self.search_form(self.request.POST, request=self.request)
        try:
            if form.is_valid():
                sqs = self.make_query(form.cleaned_data).query.load_all().order_by('-date')[:120]
                results = []
                search_weight = form.cleaned_data.get('search_weight')
                for p in sqs:
                    post = p.object
                    if search_weight and post.thread.weight not in search_weight:
                        continue
                    try:
                        self.request.acl.threads.allow_post_view(self.request.user, post.thread, post)
                        results.append(post.pk)
                    except ACLError404:
                        pass

                if self.request.user.is_authenticated():
                    self.request.user.last_search = timezone.now()
                    self.request.user.save(force_update=True)
                if self.request.user.is_anonymous():
                    self.request.session['last_search'] = timezone.now()

                self.request.session['search_form_data'] = {'form': self.search_route, 'data': form.cleaned_data}

                if not results:
                    raise SearchException(_("Search returned no results. Change search query and try again."))

                self.request.session['search_results'] = {
                                                          'search_query': form.cleaned_data['search_query'],
                                                          'search_route': self.search_route,
                                                          'search_in': self.request.POST.get('search_in'),
                                                          'search_author': self.request.POST.get('search_author'),
                                                          'search_thread_titles': self.request.POST.get('search_thread_titles'),
                                                          'search_results': results,
                                                          }
                try:
                    self.request.session['search_results']['search_thread'] = self.thread_clean
                except AttributeError:
                    pass
                return redirect(reverse('search_results'))
            else:
                raise SearchException(form.errors['__all__'][0])
        except SearchException as e:
            message = Message(e)

        return self.render_to_response(self.search_route, form,
                                       {
                                        'message': message,
                                        'search_result': self.request.session.get('search_results')
                                       })


    def __new__(cls, request, **kwargs):
        obj = super(ViewBase, cls).__new__(cls)
        return obj(request, **kwargs)

    def __call__(self, request, **kwargs):
        self.search_route = self.default_search_route
        self.search_form = self.default_search_form
        try:
            self.request = request
            if request.user.is_crawler():
                raise ACLError404()
            self.check_acl()
            if not request.acl.search.can_search():
                raise ACLError403(_("You don't have permission to search community."))
            if self.request.method == "POST":
                return self.search(request)
            return self.draw_form(request)
        except ACLError403 as e:
            return error403(request, unicode(e))
        except ACLError404 as e:
            return error404(request, unicode(e))


class QuickSearchView(ViewBase):
    default_search_route = 'search_quick'
    default_search_form = QuickSearchForm


class SearchForumsView(ViewBase):
    default_search_route = 'search_forums'
    default_search_form = ForumsSearchForm


class SearchPrivateThreadsView(ViewBase):
    default_search_route = 'search_private_threads'
    default_search_form = PrivateThreadsSearchForm

    def check_acl(self):
        if not self.request.acl.private_threads.can_participate():
            raise ACLError404()


class SearchReportsView(ViewBase):
    default_search_route = 'search_reports'
    default_search_form = ReportsSearchForm

    def check_acl(self):
        if not self.request.acl.reports.can_handle():
            raise ACLError404()


class SearchResultsView(object):
    def __new__(cls, request, **kwargs):
        obj = super(SearchResultsView, cls).__new__(cls)
        return obj(request, **kwargs)

    def __call__(self, request, **kwargs):
        try:
            if request.user.is_crawler():
                raise ACLError404()
            if not request.acl.search.can_search():
                raise ACLError403(_("You don't have permission to search community."))
            self.request = request
            return self.call(**kwargs)
        except ACLError403 as e:
            return error403(request, unicode(e))
        except ACLError404 as e:
            return error404(request, unicode(e))

    def call(self, **kwargs):
        result = self.request.session.get('search_results')
        if not result:
            return error404(self.request, _("No search results were found."))

        items = result['search_results']
        items_total = len(items);
        try:
            pagination = make_pagination(kwargs.get('page', 0), items_total, 12)
        except Http404:
            return redirect(reverse('search_results'))

        return render_to_response('search/results.html',
                                  {
                                   'search_in': result.get('search_in'),
                                   'search_route': result.get('search_route'),
                                   'search_query': result['search_query'],
                                   'search_author': result.get('search_author'),
                                   'search_thread_titles': result.get('search_thread_titles'),
                                   'search_thread': result.get('search_thread'),
                                   'results': Post.objects.filter(id__in=items).select_related('forum', 'thread', 'user').order_by('-pk')[pagination['start']:pagination['stop']],
                                   'items_total': items_total,
                                   'pagination': pagination,
                                  },
                                  context_instance=RequestContext(self.request))