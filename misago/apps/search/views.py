from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from haystack.query import RelatedSearchQuerySet
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
    results_route = 'search_results'
    advanced_route = None

    def check_acl(self):
        pass

    def queryset(self):
        pass

    def search_form_type(self):
        return QuickSearchForm

    def render_to_response(self, template, form, context):
        context.update({
                        'form': FormFields(form),
                        'search_route': self.search_route,
                        'results_route': self.results_route,
                        'search_advanced': self.advanced_route,
                        'disable_search': True,
                        })
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


class SearchBaseView(ViewBase):
    def call(self, **kwargs):
        form_type = self.search_form_type()
        if self.request.method != "POST":
            form = self.search_form_type()(request=self.request)
            return self.render_to_response('home', form,  
                                           {
                                            'search_result': self.request.session.get(self.results_route),
                                           })
        
        try:
            form = self.search_form_type()(self.request.POST, request=self.request)
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
                sqs = RelatedSearchQuerySet().auto_query(form.cleaned_data['search_query']).order_by('-id').load_all()
                sqs = sqs.load_all_queryset(Post, self.queryset().filter(deleted=False).filter(moderated=False).select_related('thread', 'forum', 'user'))[:60]

                if self.request.user.is_authenticated():
                    self.request.user.last_search = timezone.now()
                    self.request.user.save(force_update=True)
                if self.request.user.is_anonymous():
                    self.request.session['last_search'] = timezone.now()

                if not sqs:
                    raise SearchException(_("Search returned no results. Change search query and try again."))
                self.request.session[self.results_route] = {
                                                               'search_query': form.cleaned_data['search_query'],
                                                               'search_results': [p.object for p in sqs],
                                                               }
                return redirect(reverse(self.results_route))
            else:
                if 'search_query' in form.errors:
                    raise SearchException(form.errors['search_query'][0])
                raise SearchException(form.errors['__all__'][0])
        except SearchException as e:
            return self.render_to_response('error', form,  
                                           {'message': unicode(e)})


class ResultsBaseView(ViewBase):
    def call(self, **kwargs):
        result = self.request.session.get(self.results_route)
        if not result:
            form = self.search_form_type()(request=self.request)
            return self.render_to_response('error', form,  
                                           {'message': _("No search results were found.")})

        items = result['search_results']
        items_total = len(items);
        try:
            pagination = make_pagination(kwargs.get('page', 0), items_total, 12)
        except Http404:
            return redirect(reverse(self.search_route))

        form = self.search_form_type()(request=self.request, initial={'search_query': result['search_query']})
        return self.render_to_response('results', form,  
                                       {
                                        'search_query': result['search_query'],
                                        'results': items[pagination['start']:pagination['stop']],
                                        'items_total': items_total,
                                        'pagination': pagination,
                                       })