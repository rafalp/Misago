from django.db import models

from ...conf import settings


class ThreadParticipantManager(models.Manager):
    def set_owner(self, thread, user):
        ThreadParticipant.objects.filter(thread=thread, is_owner=True).update(
            is_owner=False
        )

        self.remove_participant(thread, user)

        ThreadParticipant.objects.create(thread=thread, user=user, is_owner=True)

    def add_participants(self, thread, users):
        bulk = []
        for user in users:
            bulk.append(ThreadParticipant(thread=thread, user=user, is_owner=False))

        ThreadParticipant.objects.bulk_create(bulk)

    def remove_participant(self, thread, user):
        ThreadParticipant.objects.filter(thread=thread, user=user).delete()


class ThreadParticipant(models.Model):
    thread = models.ForeignKey("misago_threads.Thread", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)

    objects = ThreadParticipantManager()
