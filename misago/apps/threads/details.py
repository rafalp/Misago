from django.template import RequestContext
from misago.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.threadtype.details import ExtraBaseView, DetailsBaseView, KarmaVotesBaseView
from misago.apps.threads.mixins import TypeMixin

class DetailsView(DetailsBaseView, TypeMixin):
    pass


class KarmaVotesView(KarmaVotesBaseView, TypeMixin):
    pass


class PollVotesView(ExtraBaseView, TypeMixin):
    def fetch_target(self):
        self.fetch_thread()
        self.fetch_poll()

    def fetch_poll(self):
        if not self.thread.poll:
            raise ACLError404(_('Selected poll could not be found.'))
        self.poll = self.thread.poll

    def check_acl(self):
        self.request.acl.threads.allow_see_poll_votes(self.forum, self.poll)

    def response(self):
        options = self.poll.option_set.all().order_by('-votes')
        options_dict = {}
        for option in options:
            option.votes_list = []
            options_dict[option.pk] = option

        for vote in self.poll.vote_set.filter(option__isnull=False).iterator():
            options_dict[vote.option_id].votes_list.append(vote)

        return render_to_response('threads/poll_votes.html',
                                  self._template_vars({
                                        'forum': self.forum,
                                        'parents': self.parents,
                                        'thread': self.thread,
                                        'poll': self.poll,
                                        'options': options,
                                        'user_votes': [x.option_id for x in self.request.user.pollvote_set.filter(poll=self.poll)] if self.request.user.is_authenticated() else []
                                      }),
                                  context_instance=RequestContext(self.request))