from urlparse import urlparse
from django.core.urlresolvers import resolve
from django.db.models import Q
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet, RelatedSearchQuerySet
from misago.acl.exceptions import ACLError403, ACLError404
from misago.models import Forum, Thread, Post, User

class SearchException(Exception):
    def __init__(self, message=None, suggestion=None):
        self.message = message
        self.suggestion = suggestion

    def __unicode__(self):
         return self.message


class SearchQuery(object):
    def __init__(self, raw_query=None):
        """
        Build search query object
        """
        if raw_query:
            self.parse_query(raw_query)

    def parse_query(self, raw_query):
        """
        Parse raw search query into dict of lists of words that should be found and cant be found in string
        """
        self.criteria = {'+': [], '-': []}
        for word in unicode(raw_query).split():
            # Trim word and skip it if its empty
            word = unicode(word).strip().lower()
            if len(word) == 0:
                pass

            # Find word mode
            mode = '+'
            if word[0] == '-':
                mode = '-'
                word = unicode(word[1:]).strip()

            # Strip extra crap
            word = ''.join(e for e in word if e.isalnum())

            # Slice word?
            if len(word) <= 3:
                raise SearchException(_("One or more search phrases are shorter than four characters."))
            if mode == '+':
                if len(word) == 5:
                    word = word[0:-1]
                if len(word) == 6:
                    word = word[0:-2]
                if len(word) > 6:
                    word = word[0:-3]
            self.criteria[mode].append(word)

        # Complain that there are no positive matches
        if not self.criteria['+'] and not self.criteria['-']:
            raise SearchException(_("Search query is invalid."))

    def search(self, value):
        """
        See if value meets search criteria, return True for success and False otherwhise
        """
        try:
            value = unicode(value).strip().lower()
            # Search for only
            if self.criteria['+'] and not self.criteria['-']:
               return self.search_for(value)
            # Search against only
            if self.criteria['-'] and not self.criteria['+']:
               return self.search_against(value)
            # Search if contains for values but not against values
            return self.search_for(value) and not self.search_against(value)
        except AttributeError:
            raise SearchException(_("You have to define search query before you will be able to search."))

    def search_for(self, value):
        """
        See if value is required
        """
        for word in self.criteria['+']:
            if value.find(word) != -1:
                return True
        return False

    def search_against(self, value):
        """
        See if value is forbidden
        """
        for word in self.criteria['-']:
            if value.find(word) != -1:
                return True
        return False


class MisagoSearchQuerySet(object):
    def __init__(self, user, acl):
        self._content = None
        self._thread_start = None
        self._thread_name = None
        self._user_name = None
        self._after = None
        self._before = None
        self._children = None
        self._threads = None
        self._forums = None

        self.user = user
        self.acl = acl

    def search_in(self, target):
        try:
            self.allow_forum_search(target)
        except AttributeError:
            self.allow_thread_search(target)

    def allow_forum_search(self, forum):
        if forum.special == 'private_threads':
            if not self.acl.private_threads.can_participate():
                raise ACLError403()
            if self.acl.private_threads.is_mod():
                self._threads = [t.pk for t in forum.thread_set.filter(Q(participants__id=self.user.pk) | Q(replies_reported__gt=0)).iterator()]
            else:
                self._threads = [t.pk for t in forum.thread_set.filter(participants__id=self.user.pk).iterator()]
        elif forum.special == 'reports':
            if not self.acl.reports.can_handle():
                raise ACLError403()
            self._forums = [forum.pk]
        else:
            self._forums = Forum.objects.readable_forums(self.acl)

    def allow_thread_search(self, thread):
        self.allow_forum_search(thread.forum)
        if thread.forum.special == 'private_threads':
            if thread.pk in self._threads:
                self._threads = [thread.pk]
            else:
                raise ACLError404()
        self._threads = [thread.pk]

    def search_content(self, query):
        self._content = query

    def restrict_threads(self, threads=None):
        self._threads = threads

    def search_thread_name_link(self, query):
        try:
            link = resolve(urlparse(query).path)
            thread = Thread.objects.get(pk=link.kwargs['thread'])
            self.allow_thread_search(thread)
        except (Http404, KeyError, Thread.DoesNotExist):
            self._thread_name = query

    def search_thread_titles(self, value=True):
        self._thread_start = value

    def search_thread_name(self, query):
        self._thread_name = query

    def search_user_name(self, query):
        self._user_name = query

    def search_after(self, datetime):
        self._after = datetime

    def search_before(self, datetime):
        self._before = datetime

    def in_forums(self, forums):
        self._forums = forums

    @property
    def query(self):
        try:
            return self._searchquery
        except AttributeError:
            pass

        sqs = SearchQuerySet()

        if self._content:
            sqs = sqs.auto_query(self._content)

        if self._thread_name:
            sqs = sqs.filter(thread_name=AutoQuery(self._thread_name))
            if self._thread_start:
                sqs = sqs.filter(start_post=1)

        if self._user_name:
            sqs = sqs.filter(username=self._user_name)

        if self._before:
            sqs = sqs.filter(date__lte=self._before)

        if self._after:
            sqs = sqs.filter(date__gte=self._after)

        if self._threads:
            sqs = sqs.filter(thread__in=self._threads)

        if self._forums:
            sqs = sqs.filter(forum__in=self._forums)

        self._searchquery = sqs
        return self._searchquery
