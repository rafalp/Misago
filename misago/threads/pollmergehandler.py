from django.utils.translation import ugettext as _

from misago.threads.models import Poll


class PollMergeHandler(object):
    def __init__(self, threads):
        self._list = []
        self._choices = {0: None}

        self._is_valid = False
        self._resolution = None

        self.threads = threads

        for thread in threads:
            try:
                self._list.append(thread.poll)
                self._choices[thread.poll.pk] = thread.poll
            except Poll.DoesNotExist:
                pass

        self._list.sort(key=lambda choice: choice.thread_id)

    @property
    def polls(self):
        return self._list

    def is_merge_conflict(self):
        return len(self._list) > 1

    def get_available_resolutions(self):
        resolutions = [(0, _("Delete all polls"))]
        for poll in self._list:
            resolutions.append((poll.pk, poll.question))
        return resolutions

    def set_resolution(self, resolution):
        try:
            resolution_clean = int(resolution)
        except (TypeError, ValueError):
            return

        if resolution_clean in self._choices:
            self._resolution = self._choices[resolution_clean]
            self._is_valid = True

    def is_valid(self):
        return self._is_valid

    def get_resolution(self):
        return self._resolution or None
