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
        if self._cache:
            return self._cache

        try:
            self._cache = pickle.loads(base64.decodestring(self._choices_cache))
        except Exception:
            self._cache = {}

        return self._cache

    @choices_cache.setter
    def choices_cache(self, choices):
        choices_cache = {'order': [], 'choices': {}}
        for choice in choices:
            choices_cache['order'].append(choice.pk)
            choices_cache['choices'][choice.pk] = choice
        self._cache = choices_cache
        self._choices_cache = base64.encodestring(pickle.dumps(choices_cache, pickle.HIGHEST_PROTOCOL))