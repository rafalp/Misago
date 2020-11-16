from datetime import timedelta
from math import ceil

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone


class Poll(models.Model):
    category = models.ForeignKey("misago_categories.Category", on_delete=models.CASCADE)
    thread = models.OneToOneField("misago_threads.Thread", on_delete=models.CASCADE)
    poster = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL
    )
    poster_name = models.CharField(max_length=255)
    poster_slug = models.CharField(max_length=255)

    posted_on = models.DateTimeField(default=timezone.now)
    length = models.PositiveIntegerField(default=0)

    question = models.CharField(max_length=255)
    choices = JSONField()
    allowed_choices = models.PositiveIntegerField(default=1)
    allow_revotes = models.BooleanField(default=False)

    votes = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=False)

    def move(self, thread):
        if self.thread_id != thread.id:
            self.thread = thread
            self.category_id = thread.category_id
            self.save()

            self.pollvote_set.update(thread=self.thread, category_id=self.category_id)

    @property
    def ends_on(self):
        if self.length:
            return self.posted_on + timedelta(days=self.length)

    @property
    def is_over(self):
        if self.length:
            return timezone.now() > self.ends_on
        return False

    @property
    def thread_type(self):
        return self.category.thread_type

    def get_api_url(self):
        return self.thread_type.get_poll_api_url(self)

    def get_votes_api_url(self):
        return self.thread_type.get_poll_votes_api_url(self)

    def make_choices_votes_aware(self, user):
        if user.is_anonymous:
            for choice in self.choices:
                choice["selected"] = False
            return

        queryset = self.pollvote_set.filter(voter=user).values("choice_hash")
        user_votes = [v["choice_hash"] for v in queryset]

        for choice in self.choices:
            choice["selected"] = choice["hash"] in user_votes

    @property
    def has_selected_choices(self):
        for choice in self.choices:
            if choice.get("selected"):
                return True
        return False

    @property
    def view_choices(self):
        view_choices = []
        for choice in self.choices:
            if choice["votes"] and self.votes:
                proc = int(ceil(choice["votes"] * 100 / self.votes))
            else:
                proc = 0

            view_choices.append(
                {
                    "label": choice["label"],
                    "votes": choice["votes"],
                    "selected": choice["selected"],
                    "proc": proc,
                }
            )
        return view_choices
