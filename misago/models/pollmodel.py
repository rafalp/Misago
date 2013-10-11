from datetime import timedelta
from django.db import models
from django.utils import timezone
import base64
try:
    import cPickle as pickle
except ImportError:
    import pickle

class Poll(models.Model):
    forum = models.ForeignKey('Forum')
    thread = models.OneToOneField('Thread', primary_key=True)
    user = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL)
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

    @property
    def end_date(self):
        return self.start_date + timedelta(days=self.length)

    @property
    def over(self):
        if not self.length:
            return False
        return timezone.now() > self.end_date

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

    def retract_vote(self, votes):
        pass

    def make_vote(self, request, options):
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
                                     date=timezone.now(),
                                     ip=request.session.get_ip(request),
                                     agent=request.META.get('HTTP_USER_AGENT'),
                                     )
        self.choices_cache = [x for x in self.option_set.all()]