from django.db import models, transaction

from misago.conf import settings


class ThreadParticipantManager(models.Manager):
    def remove_participant(self, thread, user):
        ThreadParticipant.objects.filter(thread=thread, user=user).delete()

    @transaction.atomic
    def set_owner(self, thread, user):
        thread_owner = ThreadParticipant.objects.filter(
            thread=thread, is_owner=True)
        thread_owner.update(is_owner=False)

        self.remove_participant(thread, user)
        ThreadParticipant.objects.create(
            thread=thread,
            user=user,
            is_owner=True)

    @transaction.atomic
    def add_participant(self, thread, user, is_owner=False):
        ThreadParticipant.objects.create(
            thread=thread,
            user=user,
            is_owner=is_owner)


class ThreadParticipant(models.Model):
    thread = models.ForeignKey('misago_threads.Thread')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    is_owner = models.BooleanField(default=False)

    objects = ThreadParticipantManager()
