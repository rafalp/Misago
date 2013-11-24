from datetime import timedelta
from django.db import models
from django.utils import timezone
import base64
try:
    import cPickle as pickle
except ImportError:
    import pickle
from misago.signals import (delete_user_content, merge_thread,
                            move_forum_content, move_thread,
                            rename_user)

class Poll(models.Model):
    forum = models.ForeignKey('Forum')
    thread = models.OneToOneField('Thread', primary_key=True, related_name='poll_of')
    user = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL)
    user_name = models.CharField(max_length=255, null=True, blank=True)
    user_slug = models.SlugField(max_length=255, null=True, blank=True)
    start_date = models.DateTimeField()
    length = models.PositiveIntegerField(default=0)
    question = models.CharField(max_length=255)
    max_choices = models.PositiveIntegerField(default=0)
    _choices_cache = models.TextField(db_column='choices_cache')
    votes = models.PositiveIntegerField(default=0)
    vote_changing = models.BooleanField(default=False)
    public = models.BooleanField(default=False)

    class Meta:
        app_label = 'misago'

    def move_to(self, forum=None, thread=None):
        kwargs = {}
        if forum:
            self.forum = forum
            kwargs['forum'] = forum
        if thread:
            self.thread = thread
            kwargs['thread'] = thread
        self.vote_set.all().update(**kwargs)
        self.option_set.all().update(**kwargs)
        self.save()

    @property
    def end_date(self):
        return self.start_date + timedelta(days=self.length)

    @property
    def over(self):
        if not self.length:
            return False
        return timezone.now() > self.end_date

    def make_choices_cache(self):
        self.choices_cache = [x for x in self.option_set.all()]

    @property
    def choices_cache(self):
        try:
            return self._cache
        except AttributeError:
            pass

        try:
            self._cache = pickle.loads(base64.decodestring(self._choices_cache))
        except Exception:
            self._cache = []

        return self._cache

    @choices_cache.setter
    def choices_cache(self, choices):
        choices_cache = []
        for choice in choices:
            choices_cache.append({
                'id': choice.pk,
                'pk': choice.pk,
                'name': choice.name,
                'votes': choice.votes
            })
        self._cache = choices_cache
        self._choices_cache = base64.encodestring(pickle.dumps(choices_cache, pickle.HIGHEST_PROTOCOL))

    def retract_votes(self, votes):
        options = self.option_set.all()
        options_dict = {}
        for option in options:
            options_dict[option.pk] = option

        for vote in votes:
            if vote.option_id in options_dict:
                self.votes -= 1
                options_dict[vote.option_id].votes -= 1
        self.vote_set.filter(id__in=[x.pk for x in votes]).delete()

        for option in options:
            option.save()
        self.choices_cache = options

    def make_vote(self, request, options=None):
        try:
            len(options)
        except TypeError:
            options = (options, )

        for option in self.option_set.all():
            if option.pk in options:
                self.votes += 1
                option.votes += 1
                option.save()
                self.vote_set.create(
                                     forum_id=self.forum_id,
                                     thread_id=self.thread_id,
                                     option=option,
                                     user=request.user,
                                     user_name=request.user.username,
                                     user_slug=request.user.username_slug,
                                     date=timezone.now(),
                                     ip=request.session.get_ip(request),
                                     agent=request.META.get('HTTP_USER_AGENT'),
                                     )
        self.make_choices_cache()

    def make_empty_vote(self, request):
        self.vote_set.create(
                             forum_id=self.forum_id,
                             thread_id=self.thread_id,
                             user=request.user,
                             user_name=request.user.username,
                             user_slug=request.user.username_slug,
                             date=timezone.now(),
                             ip=request.session.get_ip(request),
                             agent=request.META.get('HTTP_USER_AGENT'),
                             )


def rename_user_handler(sender, **kwargs):
    Poll.objects.filter(user=sender).update(
                                            user_name=sender.username,
                                            user_slug=sender.username_slug,
                                            )

rename_user.connect(rename_user_handler, dispatch_uid="rename_user_poll")


def delete_user_content_handler(sender, **kwargs):
    for poll in Poll.objects.filter(user=sender).iterator():
        poll.delete()

delete_user_content.connect(delete_user_content_handler, dispatch_uid="delete_user_polls")


def move_forum_content_handler(sender, **kwargs):
    Poll.objects.filter(forum=sender).update(forum=kwargs['move_to'])

move_forum_content.connect(move_forum_content_handler, dispatch_uid="move_forum_polls")


def move_thread_handler(sender, **kwargs):
    Poll.objects.filter(thread=sender).update(forum=kwargs['move_to'])

move_thread.connect(move_thread_handler, dispatch_uid="move_thread_polls")